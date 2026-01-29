# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Source code for examples.space_invaders.space_invaders

```
import curses
import logging
import random
import re
import textwrap
import time

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

logging.basicConfig(
    filename="space_invaders.log",
    format="%(asctime)s,%(msecs)03d %(levelname)-5.5s %(message)s",
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base = declarative_base()

WINDOW_LEFT = 10
WINDOW_TOP = 2
WINDOW_WIDTH = 70
WINDOW_HEIGHT = 34
VERT_PADDING = 2
HORIZ_PADDING = 5
ENEMY_VERT_SPACING = 4
MAX_X = WINDOW_WIDTH - HORIZ_PADDING
MAX_Y = WINDOW_HEIGHT - VERT_PADDING
LEFT_KEY = ord("j")
RIGHT_KEY = ord("l")
FIRE_KEY = ord(" ")
PAUSE_KEY = ord("p")

COLOR_MAP = {
    "K": curses.COLOR_BLACK,
    "B": curses.COLOR_BLUE,
    "C": curses.COLOR_CYAN,
    "G": curses.COLOR_GREEN,
    "M": curses.COLOR_MAGENTA,
    "R": curses.COLOR_RED,
    "W": curses.COLOR_WHITE,
    "Y": curses.COLOR_YELLOW,
}

class Glyph(Base):
    """Describe a "glyph", a graphical element
    to be painted on the screen.

    """

    __tablename__ = "glyph"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    data = Column(String)
    alt_data = Column(String)
    __mapper_args__ = {"polymorphic_on": type}

    def __init__(self, name, img, alt=None):
        self.name = name
        self.data, self.width, self.height = self._encode_glyph(img)
        if alt is not None:
            self.alt_data, alt_w, alt_h = self._encode_glyph(alt)

    def _encode_glyph(self, img):
        """Receive a textual description of the glyph and
        encode into a format understood by
        GlyphCoordinate.render().

        """
        img = re.sub(r"^\n", "", textwrap.dedent(img))
        color = "W"
        lines = [line.rstrip() for line in img.split("\n")]
        data = []
        for line in lines:
            render_line = []
            line = list(line)
            while line:
                char = line.pop(0)
                if char == "#":
                    color = line.pop(0)
                    continue
                render_line.append((color, char))
            data.append(render_line)
        width = max([len(rl) for rl in data])
        data = "".join(
            "".join("%s%s" % (color, char) for color, char in render_line)
            + ("W " * (width - len(render_line)))
            for render_line in data
        )
        return data, width, len(lines)

    def glyph_for_state(self, coord, state):
        """Return the appropriate data representation
        for this Glyph, based on the current coordinates
        and state.

        Subclasses may override this to provide animations.

        """
        return self.data

class GlyphCoordinate(Base):
    """Describe a glyph rendered at a certain x, y coordinate.

    The GlyphCoordinate may also include optional values
    such as the tick at time of render, a label, and a
    score value.

    """

    __tablename__ = "glyph_coordinate"
    id = Column(Integer, primary_key=True)
    glyph_id = Column(Integer, ForeignKey("glyph.id"))
    x = Column(Integer)
    y = Column(Integer)
    tick = Column(Integer)
    label = Column(String)
    score = Column(Integer)
    glyph = relationship(Glyph, innerjoin=True)

    def __init__(
        self, session, glyph_name, x, y, tick=None, label=None, score=None
    ):
        self.glyph = session.query(Glyph).filter_by(name=glyph_name).one()
        self.x = x
        self.y = y
        self.tick = tick
        self.label = label
        self.score = score
        session.add(self)

    def render(self, window, state):
        """Render the Glyph at this position."""

        col = 0
        row = 0
        glyph = self.glyph
        data = glyph.glyph_for_state(self, state)
        for color, char in [
            (data[i], data[i + 1]) for i in range(0, len(data), 2)
        ]:
            x = self.x + col
            y = self.y + row
            if 0 <= x <= MAX_X and 0 <= y <= MAX_Y:
                window.addstr(
                    y + VERT_PADDING,
                    x + HORIZ_PADDING,
                    char,
                    _COLOR_PAIRS[color],
                )
            col += 1
            if col == glyph.width:
                col = 0
                row += 1
        if self.label:
            self._render_label(window, False)

    def _render_label(self, window, blank):
        label = self.label if not blank else " " * len(self.label)
        if self.x + self.width + len(self.label) < MAX_X:
            window.addstr(self.y, self.x + self.width, label)
        else:
            window.addstr(self.y, self.x - len(self.label), label)

    def blank(self, window):
        """Render a blank box for this glyph's position and size."""

        glyph = self.glyph
        x = min(max(self.x, 0), MAX_X)
        width = min(glyph.width, MAX_X - x) or 1
        for y_a in range(self.y, self.y + glyph.height):
            y = y_a
            window.addstr(y + VERT_PADDING, x + HORIZ_PADDING, " " * width)

        if self.label:
            self._render_label(window, True)

    @hybrid_property
    def width(self):
        return self.glyph.width

    @width.expression
    def width(cls):
        return Glyph.width

    @hybrid_property
    def height(self):
        return self.glyph.height

    @height.expression
    def height(cls):
        return Glyph.height

    @hybrid_property
    def bottom_bound(self):
        return self.y + self.height >= MAX_Y

    @hybrid_property
    def top_bound(self):
        return self.y <= 0

    @hybrid_property
    def left_bound(self):
        return self.x <= 0

    @hybrid_property
    def right_bound(self):
        return self.x + self.width >= MAX_X

    @hybrid_property
    def right_edge_bound(self):
        return self.x > MAX_X

    @hybrid_method
    def intersects(self, other):
        """Return True if this GlyphCoordinate intersects with
        the given GlyphCoordinate."""

        return ~(
            (self.x + self.width < other.x) | (self.x > other.x + other.width)
        ) & ~(
            (self.y + self.height < other.y)
            | (self.y > other.y + other.height)
        )

class EnemyGlyph(Glyph):
    """Describe an enemy."""

    __mapper_args__ = {"polymorphic_identity": "enemy"}

class ArmyGlyph(EnemyGlyph):
    """Describe an enemy that's part of the "army"."""

    __mapper_args__ = {"polymorphic_identity": "army"}

    def glyph_for_state(self, coord, state):
        if state["flip"]:
            return self.alt_data
        else:
            return self.data

class SaucerGlyph(EnemyGlyph):
    """Describe the enemy saucer flying overhead."""

    __mapper_args__ = {"polymorphic_identity": "saucer"}

    def glyph_for_state(self, coord, state):
        if state["flip"] == 0:
            return self.alt_data
        else:
            return self.data

class MessageGlyph(Glyph):
    """Describe a glyph for displaying a message."""

    __mapper_args__ = {"polymorphic_identity": "message"}

class PlayerGlyph(Glyph):
    """Describe a glyph representing the player."""

    __mapper_args__ = {"polymorphic_identity": "player"}

class MissileGlyph(Glyph):
    """Describe a glyph representing a missile."""

    __mapper_args__ = {"polymorphic_identity": "missile"}

class SplatGlyph(Glyph):
    """Describe a glyph representing a "splat"."""

    __mapper_args__ = {"polymorphic_identity": "splat"}

    def glyph_for_state(self, coord, state):
        age = state["tick"] - coord.tick
        if age > 5:
            return self.alt_data
        else:
            return self.data

def init_glyph(session):
    """Create the glyphs used during play."""

    enemy1 = ArmyGlyph(
        "enemy1",
        """
         #W-#B^#R-#B^#W-
         #G|   |
        """,
        """
         #W>#B^#R-#B^#W<
         #G^   ^
        """,
    )

    enemy2 = ArmyGlyph(
        "enemy2",
        """
         #W***
        #R<#C~~~#R>
        """,
        """
         #W@@@
        #R<#C---#R>
        """,
    )

    enemy3 = ArmyGlyph(
        "enemy3",
        """
        #Y((--))
        #M-~-~-~
        """,
        """
        #Y[[--]]
        #M~-~-~-
        """,
    )

    saucer = SaucerGlyph(
        "saucer",
        """#R~#Y^#R~#G<<((=#WOO#G=))>>""",
        """#Y^#R~#Y^#G<<((=#WOO#G=))>>""",
    )

    splat1 = SplatGlyph(
        "splat1",
        """
             #WVVVVV
            #W> #R*** #W<
             #W^^^^^
        """,
        """
                #M|
             #M- #Y+++ #M-
                #M|
        """,
    )

    ship = PlayerGlyph(
        "ship",
        """
       #Y^
     #G=====
    """,
    )

    missile = MissileGlyph(
        "missile",
        """
        |
    """,
    )

    start = MessageGlyph(
        "start_message",
        "J = move left; L = move right; SPACE = fire\n"
        "           #GPress any key to start",
    )
    lose = MessageGlyph("lose_message", "#YY O U  L O S E ! ! !")
    win = MessageGlyph("win_message", "#RL E V E L  C L E A R E D ! ! !")
    paused = MessageGlyph(
        "pause_message", "#WP A U S E D\n#GPress P to continue"
    )
    session.add_all(
        [
            enemy1,
            enemy2,
            enemy3,
            ship,
            saucer,
            missile,
            start,
            lose,
            win,
            paused,
            splat1,
        ]
    )

def setup_curses():
    """Setup terminal/curses state."""

    window = curses.initscr()
    curses.noecho()

    window = curses.newwin(
        WINDOW_HEIGHT + (VERT_PADDING * 2),
        WINDOW_WIDTH + (HORIZ_PADDING * 2),
        WINDOW_TOP - VERT_PADDING,
        WINDOW_LEFT - HORIZ_PADDING,
    )
    curses.start_color()

    global _COLOR_PAIRS
    _COLOR_PAIRS = {}
    for i, (k, v) in enumerate(COLOR_MAP.items(), 1):
        curses.init_pair(i, v, curses.COLOR_BLACK)
        _COLOR_PAIRS[k] = curses.color_pair(i)
    return window

def init_positions(session):
    """Establish a new field of play.

    This generates GlyphCoordinate objects
    and persists them to the database.

    """

    # delete all existing coordinates
    session.query(GlyphCoordinate).delete()

    session.add(
        GlyphCoordinate(
            session, "ship", WINDOW_WIDTH // 2 - 2, WINDOW_HEIGHT - 4
        )
    )

    arrangement = (
        ("enemy3", 50),
        ("enemy2", 25),
        ("enemy1", 10),
        ("enemy2", 25),
        ("enemy1", 10),
    )
    for ship_vert, (etype, score) in zip(
        range(5, 30, ENEMY_VERT_SPACING), arrangement
    ):
        for ship_horiz in range(0, 50, 10):
            session.add(
                GlyphCoordinate(
                    session, etype, ship_horiz, ship_vert, score=score
                )
            )

def draw(session, window, state):
    """Load all current GlyphCoordinate objects from the
    database and render.

    """
    for gcoord in session.query(GlyphCoordinate).options(
        joinedload(GlyphCoordinate.glyph)
    ):
        gcoord.render(window, state)
    window.addstr(1, WINDOW_WIDTH - 5, "Score: %.4d" % state["score"])
    window.move(0, 0)
    window.refresh()

def check_win(session, state):
    """Return the number of army glyphs remaining -
    the player wins if this is zero."""

    return (
        session.query(func.count(GlyphCoordinate.id))
        .join(GlyphCoordinate.glyph.of_type(ArmyGlyph))
        .scalar()
    )

def check_lose(session, state):
    """Return the number of army glyphs either colliding
    with the player or hitting the bottom of the screen.

    The player loses if this is non-zero."""

    player = state["player"]
    return (
        session.query(GlyphCoordinate)
        .join(GlyphCoordinate.glyph.of_type(ArmyGlyph))
        .filter(
            GlyphCoordinate.intersects(player) | GlyphCoordinate.bottom_bound
        )
        .count()
    )

def render_message(session, window, msg, x, y):
    """Render a message glyph.

    Clears the area beneath the message first
    and assumes the display will be paused
    afterwards.

    """
    # create message box
    msg = GlyphCoordinate(session, msg, x, y)

    # clear existing glyphs which intersect
    for gly in (
        session.query(GlyphCoordinate)
        .join(GlyphCoordinate.glyph)
        .filter(GlyphCoordinate.intersects(msg))
    ):
        gly.blank(window)

    # render
    msg.render(window, {})
    window.refresh()
    return msg

def win(session, window, state):
    """Handle the win case."""
    render_message(session, window, "win_message", 15, 15)
    time.sleep(2)
    start(session, window, state, True)

def lose(session, window, state):
    """Handle the lose case."""
    render_message(session, window, "lose_message", 15, 15)
    time.sleep(2)
    start(session, window, state)

def pause(session, window, state):
    """Pause the game."""
    msg = render_message(session, window, "pause_message", 15, 15)
    prompt(window)
    msg.blank(window)
    session.delete(msg)

def prompt(window):
    """Display a prompt, quashing any keystrokes
    which might have remained."""

    window.move(0, 0)
    window.nodelay(1)
    window.getch()
    window.nodelay(0)
    window.getch()
    window.nodelay(1)

def move_army(session, window, state):
    """Update the army position based on the current
    size of the field."""
    speed = 30 // 25 * state["num_enemies"]

    flip = (state["tick"] % speed) == 0

    if not flip:
        return
    else:
        state["flip"] = not state["flip"]

    x_slide = 1

    # get the lower/upper boundaries of the army
    # along the X axis.
    min_x, max_x = (
        session.query(
            func.min(GlyphCoordinate.x),
            func.max(GlyphCoordinate.x + GlyphCoordinate.width),
        )
        .join(GlyphCoordinate.glyph.of_type(ArmyGlyph))
        .first()
    )

    if min_x is None or max_x is None:
        # no enemies
        return

    direction = state["army_direction"]
    move_y = False
    if direction == 0 and max_x + x_slide >= MAX_X:
        direction = state["army_direction"] = 1
        move_y = True
    elif direction == 1 and min_x - x_slide <= 0:
        direction = state["army_direction"] = 0
        move_y = True

    for enemy_g in session.query(GlyphCoordinate).join(
        GlyphCoordinate.glyph.of_type(ArmyGlyph)
    ):
        enemy_g.blank(window)

        if move_y:
            enemy_g.y += 1
        elif direction == 0:
            enemy_g.x += x_slide
        elif direction == 1:
            enemy_g.x -= x_slide

def move_player(session, window, state):
    """Receive player input and adjust state."""

    ch = window.getch()
    if ch not in (LEFT_KEY, RIGHT_KEY, FIRE_KEY, PAUSE_KEY):
        return
    elif ch == PAUSE_KEY:
        pause(session, window, state)
        return

    player = state["player"]
    if ch == RIGHT_KEY and not player.right_bound:
        player.blank(window)
        player.x += 1
    elif ch == LEFT_KEY and not player.left_bound:
        player.blank(window)
        player.x -= 1
    elif ch == FIRE_KEY and state["missile"] is None:
        state["missile"] = GlyphCoordinate(
            session, "missile", player.x + 3, player.y - 1
        )

def move_missile(session, window, state):
    """Update the status of the current missile, if any."""

    if state["missile"] is None or state["tick"] % 2 != 0:
        return

    missile = state["missile"]

    # locate enemy glyphs which intersect with the
    # missile's current position; i.e. a hit
    glyph = (
        session.query(GlyphCoordinate)
        .join(GlyphCoordinate.glyph.of_type(EnemyGlyph))
        .filter(GlyphCoordinate.intersects(missile))
        .first()
    )
    missile.blank(window)
    if glyph or missile.top_bound:
        # missile is done
        session.delete(missile)
        state["missile"] = None
        if glyph:
            # score!
            score(session, window, state, glyph)
    else:
        # move missile up one character.
        missile.y -= 1

def move_saucer(session, window, state):
    """Update the status of the saucer."""

    saucer_interval = 500
    saucer_speed_interval = 4
    if state["saucer"] is None and state["tick"] % saucer_interval != 0:
        return

    if state["saucer"] is None:
        state["saucer"] = saucer = GlyphCoordinate(
            session, "saucer", -6, 1, score=random.randrange(100, 600, 100)
        )
    elif state["tick"] % saucer_speed_interval == 0:
        saucer = state["saucer"]
        saucer.blank(window)
        saucer.x += 1
        if saucer.right_edge_bound:
            session.delete(saucer)
            state["saucer"] = None

def update_splat(session, window, state):
    """Render splat animations."""

    for splat in session.query(GlyphCoordinate).join(
        GlyphCoordinate.glyph.of_type(SplatGlyph)
    ):
        age = state["tick"] - splat.tick
        if age > 10:
            splat.blank(window)
            session.delete(splat)
        else:
            splat.render(window, state)

def score(session, window, state, glyph):
    """Process a glyph intersecting with a missile."""

    glyph.blank(window)
    session.delete(glyph)
    if state["saucer"] is glyph:
        state["saucer"] = None
    state["score"] += glyph.score
    # render a splat !
    GlyphCoordinate(
        session,
        "splat1",
        glyph.x,
        glyph.y,
        tick=state["tick"],
        label=str(glyph.score),
    )

def update_state(session, window, state):
    """Update all state for each game tick."""

    num_enemies = state["num_enemies"] = check_win(session, state)
    if num_enemies == 0:
        win(session, window, state)
    elif check_lose(session, state):
        lose(session, window, state)
    else:
        # update the tick counter.
        state["tick"] += 1
        move_player(session, window, state)
        move_missile(session, window, state)
        move_army(session, window, state)
        move_saucer(session, window, state)
        update_splat(session, window, state)

def start(session, window, state, continue_=False):
    """Start a new field of play."""

    render_message(session, window, "start_message", 15, 20)
    prompt(window)

    init_positions(session)

    player = (
        session.query(GlyphCoordinate)
        .join(GlyphCoordinate.glyph.of_type(PlayerGlyph))
        .one()
    )
    state.update(
        {
            "field_pos": 0,
            "alt": False,
            "tick": 0,
            "missile": None,
            "saucer": None,
            "player": player,
            "army_direction": 0,
            "flip": False,
        }
    )
    if not continue_:
        state["score"] = 0

    window.clear()
    window.box()
    draw(session, window, state)

def main():
    """Initialize the database and establish the game loop."""

    e = create_engine("sqlite://")
    Base.metadata.create_all(e)
    session = Session(e)
    init_glyph(session)
    session.commit()
    window = setup_curses()
    state = {}
    start(session, window, state)
    while True:
        update_state(session, window, state)
        draw(session, window, state)
        time.sleep(0.01)

if __name__ == "__main__":
    main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_history.history_meta

```
"""Versioned mixin class and other utilities."""

import datetime

from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import event
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import select
from sqlalchemy import util
from sqlalchemy.orm import attributes
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.exc import UnmappedColumnError
from sqlalchemy.orm.relationships import RelationshipProperty

def col_references_table(col, table):
    for fk in col.foreign_keys:
        if fk.references(table):
            return True
    return False

def _is_versioning_col(col):
    return "version_meta" in col.info

def _history_mapper(local_mapper):
    cls = local_mapper.class_

    if cls.__dict__.get("_history_mapper_configured", False):
        return

    cls._history_mapper_configured = True

    super_mapper = local_mapper.inherits
    polymorphic_on = None
    super_fks = []
    properties = util.OrderedDict()

    if super_mapper:
        super_history_mapper = super_mapper.class_.__history_mapper__
    else:
        super_history_mapper = None

    if (
        not super_mapper
        or local_mapper.local_table is not super_mapper.local_table
    ):
        version_meta = {"version_meta": True}  # add column.info to identify
        # columns specific to versioning

        history_table = local_mapper.local_table.to_metadata(
            local_mapper.local_table.metadata,
            name=local_mapper.local_table.name + "_history",
        )
        for idx in history_table.indexes:
            if idx.name is not None:
                idx.name += "_history"
            idx.unique = False

        for orig_c, history_c in zip(
            local_mapper.local_table.c, history_table.c
        ):
            orig_c.info["history_copy"] = history_c
            history_c.unique = False
            history_c.default = history_c.server_default = None
            history_c.autoincrement = False

            if super_mapper and col_references_table(
                orig_c, super_mapper.local_table
            ):
                assert super_history_mapper is not None
                super_fks.append(
                    (
                        history_c.key,
                        list(super_history_mapper.local_table.primary_key)[0],
                    )
                )
            if orig_c is local_mapper.polymorphic_on:
                polymorphic_on = history_c

            orig_prop = local_mapper.get_property_by_column(orig_c)
            # carry over column re-mappings
            if (
                len(orig_prop.columns) > 1
                or orig_prop.columns[0].key != orig_prop.key
            ):
                properties[orig_prop.key] = tuple(
                    col.info["history_copy"] for col in orig_prop.columns
                )

        for const in list(history_table.constraints):
            if not isinstance(
                const, (PrimaryKeyConstraint, ForeignKeyConstraint)
            ):
                history_table.constraints.discard(const)

        # "version" stores the integer version id.  This column is
        # required.
        history_table.append_column(
            Column(
                "version",
                Integer,
                primary_key=True,
                autoincrement=False,
                info=version_meta,
            )
        )

        # "changed" column stores the UTC timestamp of when the
        # history row was created.
        # This column is optional and can be omitted.
        history_table.append_column(
            Column(
                "changed",
                DateTime,
                default=lambda: datetime.datetime.now(datetime.timezone.utc),
                info=version_meta,
            )
        )

        if super_mapper:
            super_fks.append(
                ("version", super_history_mapper.local_table.c.version)
            )

        if super_fks:
            history_table.append_constraint(
                ForeignKeyConstraint(*zip(*super_fks))
            )

    else:
        history_table = None
        super_history_table = super_mapper.local_table.metadata.tables[
            super_mapper.local_table.name + "_history"
        ]

        # single table inheritance.  take any additional columns that may have
        # been added and add them to the history table.
        for column in local_mapper.local_table.c:
            if column.key not in super_history_table.c:
                col = Column(
                    column.name, column.type, nullable=column.nullable
                )
                super_history_table.append_column(col)

    if not super_mapper:

        def default_version_from_history(context):
            # Set default value of version column to the maximum of the
            # version in history columns already present +1
            # Otherwise re-appearance of deleted rows would cause an error
            # with the next update
            current_parameters = context.get_current_parameters()
            return context.connection.scalar(
                select(
                    func.coalesce(func.max(history_table.c.version), 0) + 1
                ).where(
                    and_(
                        *[
                            history_table.c[c.name]
                            == current_parameters.get(c.name, None)
                            for c in inspect(
                                local_mapper.local_table
                            ).primary_key
                        ]
                    )
                )
            )

        local_mapper.local_table.append_column(
            Column(
                "version",
                Integer,
                # if rows are not being deleted from the main table with
                # subsequent reuse of primary key, this default can be
                # "1" instead of running a query per INSERT
                default=default_version_from_history,
                nullable=False,
            ),
            replace_existing=True,
        )
        local_mapper.add_property(
            "version", local_mapper.local_table.c.version
        )

        if cls.use_mapper_versioning:
            local_mapper.version_id_col = local_mapper.local_table.c.version

    # set the "active_history" flag
    # on on column-mapped attributes so that the old version
    # of the info is always loaded (currently sets it on all attributes)
    for prop in local_mapper.iterate_properties:
        prop.active_history = True

    super_mapper = local_mapper.inherits

    if super_history_mapper:
        bases = (super_history_mapper.class_,)

        if history_table is not None:
            properties["changed"] = (history_table.c.changed,) + tuple(
                super_history_mapper.attrs.changed.columns
            )

    else:
        bases = local_mapper.base_mapper.class_.__bases__

    versioned_cls = type(
        "%sHistory" % cls.__name__,
        bases,
        {
            "_history_mapper_configured": True,
            "__table__": history_table,
            "__mapper_args__": dict(
                inherits=super_history_mapper,
                polymorphic_identity=local_mapper.polymorphic_identity,
                polymorphic_on=polymorphic_on,
                properties=properties,
            ),
        },
    )

    cls.__history_mapper__ = versioned_cls.__mapper__

class Versioned:
    use_mapper_versioning = False
    """if True, also assign the version column to be tracked by the mapper"""

    __table_args__ = {"sqlite_autoincrement": True}
    """Use sqlite_autoincrement, to ensure unique integer values
    are used for new rows even for rows that have been deleted."""

    def __init_subclass__(cls) -> None:
        insp = inspect(cls, raiseerr=False)

        if insp is not None:
            _history_mapper(insp)
        else:

            @event.listens_for(cls, "after_mapper_constructed")
            def _mapper_constructed(mapper, class_):
                _history_mapper(mapper)

        super().__init_subclass__()

def versioned_objects(iter_):
    for obj in iter_:
        if hasattr(obj, "__history_mapper__"):
            yield obj

def create_version(obj, session, deleted=False):
    obj_mapper = object_mapper(obj)
    history_mapper = obj.__history_mapper__
    history_cls = history_mapper.class_

    obj_state = attributes.instance_state(obj)

    attr = {}

    obj_changed = False

    for om, hm in zip(
        obj_mapper.iterate_to_root(), history_mapper.iterate_to_root()
    ):
        if hm.single:
            continue

        for hist_col in hm.local_table.c:
            if _is_versioning_col(hist_col):
                continue

            obj_col = om.local_table.c[hist_col.key]

            # get the value of the
            # attribute based on the MapperProperty related to the
            # mapped column.  this will allow usage of MapperProperties
            # that have a different keyname than that of the mapped column.
            try:
                prop = obj_mapper.get_property_by_column(obj_col)
            except UnmappedColumnError:
                # in the case of single table inheritance, there may be
                # columns on the mapped table intended for the subclass only.
                # the "unmapped" status of the subclass column on the
                # base class is a feature of the declarative module.
                continue

            # expired object attributes and also deferred cols might not
            # be in the dict.  force it to load no matter what by
            # using getattr().
            if prop.key not in obj_state.dict:
                getattr(obj, prop.key)

            a, u, d = attributes.get_history(obj, prop.key)

            if d:
                attr[prop.key] = d[0]
                obj_changed = True
            elif u:
                attr[prop.key] = u[0]
            elif a:
                # if the attribute had no value.
                attr[prop.key] = a[0]
                obj_changed = True

    if not obj_changed:
        # not changed, but we have relationships.  OK
        # check those too
        for prop in obj_mapper.iterate_properties:
            if (
                isinstance(prop, RelationshipProperty)
                and attributes.get_history(
                    obj, prop.key, passive=attributes.PASSIVE_NO_INITIALIZE
                ).has_changes()
            ):
                for p in prop.local_columns:
                    if p.foreign_keys:
                        obj_changed = True
                        break
                if obj_changed is True:
                    break

    if not obj_changed and not deleted:
        return

    attr["version"] = obj.version
    hist = history_cls()
    for key, value in attr.items():
        setattr(hist, key, value)
    session.add(hist)
    obj.version += 1

def versioned_session(session):
    @event.listens_for(session, "before_flush")
    def before_flush(session, flush_context, instances):
        for obj in versioned_objects(session.dirty):
            create_version(obj, session)
        for obj in versioned_objects(session.deleted):
            create_version(obj, session, deleted=True)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_history.test_versioning

```
"""Unit tests illustrating usage of the ``history_meta.py``
module functions."""

import unittest
import warnings

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Index
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import testing
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import clear_mappers
from sqlalchemy.orm import column_property
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import deferred
from sqlalchemy.orm import exc as orm_exc
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.testing import assert_raises
from sqlalchemy.testing import AssertsCompiledSQL
from sqlalchemy.testing import eq_
from sqlalchemy.testing import eq_ignore_whitespace
from sqlalchemy.testing import is_
from sqlalchemy.testing import ne_
from sqlalchemy.testing.entities import ComparableEntity
from .history_meta import Versioned
from .history_meta import versioned_session

warnings.simplefilter("error")

class TestVersioning(AssertsCompiledSQL):
    __dialect__ = "default"

    def setUp(self):
        self.engine = engine = create_engine("sqlite://")
        self.session = Session(engine)
        self.make_base()
        versioned_session(self.session)

    def tearDown(self):
        self.session.close()
        clear_mappers()
        self.Base.metadata.drop_all(self.engine)

    def make_base(self):
        self.Base = declarative_base()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

    def test_plain(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        sc.name = "sc1modified"
        sess.commit()

        assert sc.version == 2

        SomeClassHistory = SomeClass.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory)
            .filter(SomeClassHistory.version == 1)
            .all(),
            [SomeClassHistory(version=1, name="sc1")],
        )

        sc.name = "sc1modified2"

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.version)
            .all(),
            [
                SomeClassHistory(version=1, name="sc1"),
                SomeClassHistory(version=2, name="sc1modified"),
            ],
        )

        assert sc.version == 3

        sess.commit()

        sc.name = "temp"
        sc.name = "sc1modified2"

        sess.commit()

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.version)
            .all(),
            [
                SomeClassHistory(version=1, name="sc1"),
                SomeClassHistory(version=2, name="sc1modified"),
            ],
        )

        sess.delete(sc)
        sess.commit()

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.version)
            .all(),
            [
                SomeClassHistory(version=1, name="sc1"),
                SomeClassHistory(version=2, name="sc1modified"),
                SomeClassHistory(version=3, name="sc1modified2"),
            ],
        )

    @testing.variation(
        "constraint_type",
        [
            "index_single_col",
            "composite_index",
            "explicit_name_index",
            "unique_constraint",
            "unique_constraint_naming_conv",
            "unique_constraint_explicit_name",
            "fk_constraint",
            "fk_constraint_naming_conv",
            "fk_constraint_explicit_name",
        ],
    )
    def test_index_naming(self, constraint_type):
        """test #10920"""

        if (
            constraint_type.unique_constraint_naming_conv
            or constraint_type.fk_constraint_naming_conv
        ):
            self.Base.metadata.naming_convention = {
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "fk": (
                    "fk_%(table_name)s_%(column_0_name)s"
                    "_%(referred_table_name)s"
                ),
            }

        if (
            constraint_type.fk_constraint
            or constraint_type.fk_constraint_naming_conv
            or constraint_type.fk_constraint_explicit_name
        ):

            class Related(self.Base):
                __tablename__ = "related"

                id = Column(Integer, primary_key=True)

        class SomeClass(Versioned, self.Base):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            x = Column(Integer)
            y = Column(Integer)

            # Index objects are copied and these have to have a new name
            if constraint_type.index_single_col:
                __table_args__ = (
                    Index(
                        None,
                        x,
                    ),
                )
            elif constraint_type.composite_index:
                __table_args__ = (Index(None, x, y),)
            elif constraint_type.explicit_name_index:
                __table_args__ = (Index("my_index", x, y),)
            # unique constraint objects are discarded.
            elif (
                constraint_type.unique_constraint
                or constraint_type.unique_constraint_naming_conv
            ):
                __table_args__ = (UniqueConstraint(x, y),)
            elif constraint_type.unique_constraint_explicit_name:
                __table_args__ = (UniqueConstraint(x, y, name="my_uq"),)
            # foreign key constraint objects are copied and have the same
            # name, but no database in Core has any problem with this as the
            # names are local to the parent table.
            elif (
                constraint_type.fk_constraint
                or constraint_type.fk_constraint_naming_conv
            ):
                __table_args__ = (ForeignKeyConstraint([x], [Related.id]),)
            elif constraint_type.fk_constraint_explicit_name:
                __table_args__ = (
                    ForeignKeyConstraint([x], [Related.id], name="my_fk"),
                )
            else:
                constraint_type.fail()

        eq_(
            set(idx.name + "_history" for idx in SomeClass.__table__.indexes),
            set(
                idx.name
                for idx in SomeClass.__history_mapper__.local_table.indexes
            ),
        )
        self.create_tables()

    def test_discussion_9546(self):
        class ThingExternal(Versioned, self.Base):
            __tablename__ = "things_external"
            id = Column(Integer, primary_key=True)
            external_attribute = Column(String)

        class ThingLocal(Versioned, self.Base):
            __tablename__ = "things_local"
            id = Column(
                Integer, ForeignKey(ThingExternal.id), primary_key=True
            )
            internal_attribute = Column(String)

        is_(ThingExternal.__table__, inspect(ThingExternal).local_table)

        class Thing(self.Base):
            __table__ = join(ThingExternal, ThingLocal)
            id = column_property(ThingExternal.id, ThingLocal.id)
            version = column_property(
                ThingExternal.version, ThingLocal.version
            )

        eq_ignore_whitespace(
            str(select(Thing)),
            "SELECT things_external.id, things_local.id AS id_1, "
            "things_external.external_attribute, things_external.version, "
            "things_local.version AS version_1, "
            "things_local.internal_attribute FROM things_external "
            "JOIN things_local ON things_external.id = things_local.id",
        )

    def test_w_mapper_versioning(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"
            use_mapper_versioning = True

            id = Column(Integer, primary_key=True)
            name = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        s2 = Session(sess.bind)
        sc2 = s2.query(SomeClass).first()
        sc2.name = "sc1modified"

        sc.name = "sc1modified_again"
        sess.commit()

        eq_(sc.version, 2)

        assert_raises(orm_exc.StaleDataError, s2.flush)

    def test_from_null(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = SomeClass()
        sess.add(sc)
        sess.commit()

        sc.name = "sc1"
        sess.commit()

        assert sc.version == 2

    def test_insert_null(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            boole = Column(Boolean, default=False)

        self.create_tables()
        sess = self.session
        sc = SomeClass(boole=True)
        sess.add(sc)
        sess.commit()

        sc.boole = None
        sess.commit()

        sc.boole = False
        sess.commit()

        SomeClassHistory = SomeClass.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory.boole)
            .order_by(SomeClassHistory.id)
            .all(),
            [(True,), (None,)],
        )

        eq_(sc.version, 3)

    def test_deferred(self):
        """test versioning of unloaded, deferred columns."""

        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            data = deferred(Column(String(25)))

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1", data="somedata")
        sess.add(sc)
        sess.commit()
        sess.close()

        sc = sess.query(SomeClass).first()
        assert "data" not in sc.__dict__

        sc.name = "sc1modified"
        sess.commit()

        assert sc.version == 2

        SomeClassHistory = SomeClass.__history_mapper__.class_

        eq_(
            sess.query(SomeClassHistory)
            .filter(SomeClassHistory.version == 1)
            .all(),
            [SomeClassHistory(version=1, name="sc1", data="somedata")],
        )

    def test_joined_inheritance(self):
        class BaseClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "basetable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            type = Column(String(20))

            __mapper_args__ = {
                "polymorphic_on": type,
                "polymorphic_identity": "base",
            }

        class SubClassSeparatePk(BaseClass):
            __tablename__ = "subtable1"

            id = column_property(
                Column(Integer, primary_key=True), BaseClass.id
            )
            base_id = Column(Integer, ForeignKey("basetable.id"))
            subdata1 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "sep"}

        class SubClassSamePk(BaseClass):
            __tablename__ = "subtable2"

            id = Column(Integer, ForeignKey("basetable.id"), primary_key=True)
            subdata2 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "same"}

        self.create_tables()
        sess = self.session

        sep1 = SubClassSeparatePk(name="sep1", subdata1="sep1subdata")
        base1 = BaseClass(name="base1")
        same1 = SubClassSamePk(name="same1", subdata2="same1subdata")
        sess.add_all([sep1, base1, same1])
        sess.commit()

        base1.name = "base1mod"
        same1.subdata2 = "same1subdatamod"
        sep1.name = "sep1mod"
        sess.commit()

        BaseClassHistory = BaseClass.__history_mapper__.class_
        SubClassSeparatePkHistory = (
            SubClassSeparatePk.__history_mapper__.class_
        )
        SubClassSamePkHistory = SubClassSamePk.__history_mapper__.class_
        eq_(
            sess.query(BaseClassHistory).order_by(BaseClassHistory.id).all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", version=1),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", version=1
                ),
            ],
        )

        same1.subdata2 = "same1subdatamod2"

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.version)
            .all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", version=1),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", version=1
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", version=2
                ),
            ],
        )

        base1.name = "base1mod2"
        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.version)
            .all(),
            [
                SubClassSeparatePkHistory(
                    id=1, name="sep1", type="sep", version=1
                ),
                BaseClassHistory(id=2, name="base1", type="base", version=1),
                BaseClassHistory(
                    id=2, name="base1mod", type="base", version=2
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", version=1
                ),
                SubClassSamePkHistory(
                    id=3, name="same1", type="same", version=2
                ),
            ],
        )

    def test_joined_inheritance_multilevel(self):
        class BaseClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "basetable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            type = Column(String(20))

            __mapper_args__ = {
                "polymorphic_on": type,
                "polymorphic_identity": "base",
            }

        class SubClass(BaseClass):
            __tablename__ = "subtable"

            id = column_property(
                Column(Integer, primary_key=True), BaseClass.id
            )
            base_id = Column(Integer, ForeignKey("basetable.id"))
            subdata1 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "sub"}

        class SubSubClass(SubClass):
            __tablename__ = "subsubtable"

            id = Column(Integer, ForeignKey("subtable.id"), primary_key=True)
            subdata2 = Column(String(50))

            __mapper_args__ = {"polymorphic_identity": "subsub"}

        self.create_tables()

        SubSubHistory = SubSubClass.__history_mapper__.class_
        sess = self.session
        q = sess.query(SubSubHistory)
        self.assert_compile(
            q,
            "SELECT "
            "basetable_history.name AS basetable_history_name, "
            "basetable_history.type AS basetable_history_type, "
            "subsubtable_history.version AS subsubtable_history_version, "
            "subtable_history.version AS subtable_history_version, "
            "basetable_history.version AS basetable_history_version, "
            "subtable_history.base_id AS subtable_history_base_id, "
            "subtable_history.subdata1 AS subtable_history_subdata1, "
            "subsubtable_history.id AS subsubtable_history_id, "
            "subtable_history.id AS subtable_history_id, "
            "basetable_history.id AS basetable_history_id, "
            "subsubtable_history.changed AS subsubtable_history_changed, "
            "subtable_history.changed AS subtable_history_changed, "
            "basetable_history.changed AS basetable_history_changed, "
            "subsubtable_history.subdata2 AS subsubtable_history_subdata2 "
            "FROM basetable_history "
            "JOIN subtable_history "
            "ON basetable_history.id = subtable_history.base_id "
            "AND basetable_history.version = subtable_history.version "
            "JOIN subsubtable_history ON subtable_history.id = "
            "subsubtable_history.id AND subtable_history.version = "
            "subsubtable_history.version",
        )

        ssc = SubSubClass(name="ss1", subdata1="sd1", subdata2="sd2")
        sess.add(ssc)
        sess.commit()
        eq_(sess.query(SubSubHistory).all(), [])
        ssc.subdata1 = "sd11"
        ssc.subdata2 = "sd22"
        sess.commit()
        eq_(
            sess.query(SubSubHistory).all(),
            [
                SubSubHistory(
                    name="ss1",
                    subdata1="sd1",
                    subdata2="sd2",
                    type="subsub",
                    version=1,
                )
            ],
        )
        eq_(
            ssc,
            SubSubClass(
                name="ss1", subdata1="sd11", subdata2="sd22", version=2
            ),
        )

    def test_joined_inheritance_changed(self):
        class BaseClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "basetable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            type = Column(String(20))

            __mapper_args__ = {
                "polymorphic_on": type,
                "polymorphic_identity": "base",
            }

        class SubClass(BaseClass):
            __tablename__ = "subtable"

            id = Column(Integer, ForeignKey("basetable.id"), primary_key=True)

            __mapper_args__ = {"polymorphic_identity": "sep"}

        self.create_tables()

        BaseClassHistory = BaseClass.__history_mapper__.class_
        SubClassHistory = SubClass.__history_mapper__.class_
        sess = self.session
        s1 = SubClass(name="s1")
        sess.add(s1)
        sess.commit()

        s1.name = "s2"
        sess.commit()

        actual_changed_base = sess.scalar(
            select(BaseClass.__history_mapper__.local_table.c.changed)
        )
        actual_changed_sub = sess.scalar(
            select(SubClass.__history_mapper__.local_table.c.changed)
        )
        h1 = sess.query(BaseClassHistory).first()
        eq_(h1.changed, actual_changed_base)
        eq_(h1.changed, actual_changed_sub)

        h1 = sess.query(SubClassHistory).first()
        eq_(h1.changed, actual_changed_base)
        eq_(h1.changed, actual_changed_sub)

    def test_single_inheritance(self):
        class BaseClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "basetable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            type = Column(String(50))
            __mapper_args__ = {
                "polymorphic_on": type,
                "polymorphic_identity": "base",
            }

        class SubClass(BaseClass):
            subname = Column(String(50), unique=True)
            __mapper_args__ = {"polymorphic_identity": "sub"}

        self.create_tables()
        sess = self.session

        b1 = BaseClass(name="b1")
        sc = SubClass(name="s1", subname="sc1")

        sess.add_all([b1, sc])

        sess.commit()

        b1.name = "b1modified"

        BaseClassHistory = BaseClass.__history_mapper__.class_
        SubClassHistory = SubClass.__history_mapper__.class_

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.version)
            .all(),
            [BaseClassHistory(id=1, name="b1", type="base", version=1)],
        )

        sc.name = "s1modified"
        b1.name = "b1modified2"

        eq_(
            sess.query(BaseClassHistory)
            .order_by(BaseClassHistory.id, BaseClassHistory.version)
            .all(),
            [
                BaseClassHistory(id=1, name="b1", type="base", version=1),
                BaseClassHistory(
                    id=1, name="b1modified", type="base", version=2
                ),
                SubClassHistory(id=2, name="s1", type="sub", version=1),
            ],
        )

        # test the unique constraint on the subclass
        # column
        sc.name = "modifyagain"
        sess.flush()

    def test_unique(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50), unique=True)
            data = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1", data="sc1")
        sess.add(sc)
        sess.commit()

        sc.data = "sc1modified"
        sess.commit()

        assert sc.version == 2

        sc.data = "sc1modified2"
        sess.commit()

        assert sc.version == 3

    def test_relationship(self):
        class SomeRelated(self.Base, ComparableEntity):
            __tablename__ = "somerelated"

            id = Column(Integer, primary_key=True)

        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            related_id = Column(Integer, ForeignKey("somerelated.id"))
            related = relationship("SomeRelated", backref="classes")

        SomeClassHistory = SomeClass.__history_mapper__.class_

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        assert sc.version == 1

        sr1 = SomeRelated()
        sc.related = sr1
        sess.commit()

        assert sc.version == 2

        eq_(
            sess.query(SomeClassHistory)
            .filter(SomeClassHistory.version == 1)
            .all(),
            [SomeClassHistory(version=1, name="sc1", related_id=None)],
        )

        sc.related = None

        eq_(
            sess.query(SomeClassHistory)
            .order_by(SomeClassHistory.version)
            .all(),
            [
                SomeClassHistory(version=1, name="sc1", related_id=None),
                SomeClassHistory(version=2, name="sc1", related_id=sr1.id),
            ],
        )

        assert sc.version == 3

    def test_backref_relationship(self):
        class SomeRelated(self.Base, ComparableEntity):
            __tablename__ = "somerelated"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))
            related_id = Column(Integer, ForeignKey("sometable.id"))
            related = relationship("SomeClass", backref="related")

        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)

        self.create_tables()
        sess = self.session
        sc = SomeClass()
        sess.add(sc)
        sess.commit()

        assert sc.version == 1

        sr = SomeRelated(name="sr", related=sc)
        sess.add(sr)
        sess.commit()

        assert sc.version == 1

        sr.name = "sr2"
        sess.commit()

        assert sc.version == 1

        sess.delete(sr)
        sess.commit()

        assert sc.version == 1

    def test_create_double_flush(self):
        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(30))
            other = Column(String(30))

        self.create_tables()

        sc = SomeClass()
        self.session.add(sc)
        self.session.flush()
        sc.name = "Foo"
        self.session.flush()

        assert sc.version == 2

    def test_mutate_plain_column(self):
        class Document(self.Base, Versioned):
            __tablename__ = "document"
            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String, nullable=True)
            description_ = Column("description", String, nullable=True)

        self.create_tables()

        document = Document()
        self.session.add(document)
        document.name = "Foo"
        self.session.commit()
        document.name = "Bar"
        self.session.commit()

        DocumentHistory = Document.__history_mapper__.class_
        v2 = self.session.query(Document).one()
        v1 = self.session.query(DocumentHistory).one()
        eq_(v1.id, v2.id)
        eq_(v2.name, "Bar")
        eq_(v1.name, "Foo")

    def test_mutate_named_column(self):
        class Document(self.Base, Versioned):
            __tablename__ = "document"
            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String, nullable=True)
            description_ = Column("description", String, nullable=True)

        self.create_tables()

        document = Document()
        self.session.add(document)
        document.description_ = "Foo"
        self.session.commit()
        document.description_ = "Bar"
        self.session.commit()

        DocumentHistory = Document.__history_mapper__.class_
        v2 = self.session.query(Document).one()
        v1 = self.session.query(DocumentHistory).one()
        eq_(v1.id, v2.id)
        eq_(v2.description_, "Bar")
        eq_(v1.description_, "Foo")

    def test_unique_identifiers_across_deletes(self):
        """Ensure unique integer values are used for the primary table.

        Checks whether the database assigns the same identifier twice
        within the span of a table.  SQLite will do this if
        sqlite_autoincrement is not set (e.g. SQLite's AUTOINCREMENT flag).

        """

        class SomeClass(Versioned, self.Base, ComparableEntity):
            __tablename__ = "sometable"

            id = Column(Integer, primary_key=True)
            name = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = SomeClass(name="sc1")
        sess.add(sc)
        sess.commit()

        sess.delete(sc)
        sess.commit()

        sc2 = SomeClass(name="sc2")
        sess.add(sc2)
        sess.commit()

        SomeClassHistory = SomeClass.__history_mapper__.class_

        # only one entry should exist in the history table; one()
        # ensures that
        scdeleted = sess.query(SomeClassHistory).one()

        # If sc2 has the same id that deleted sc1 had,
        # it will fail when modified or deleted
        # because of the violation of the uniqueness of the primary key on
        # sometable_history
        ne_(sc2.id, scdeleted.id)

        # If previous assertion fails, this will also fail:
        sc2.name = "sc2 modified"
        sess.commit()

    def test_external_id(self):
        class ObjectExternal(Versioned, self.Base, ComparableEntity):
            __tablename__ = "externalobjects"

            id1 = Column(String(3), primary_key=True)
            id2 = Column(String(3), primary_key=True)
            name = Column(String(50))

        self.create_tables()
        sess = self.session
        sc = ObjectExternal(id1="aaa", id2="bbb", name="sc1")
        sess.add(sc)
        sess.commit()

        sc.name = "sc1modified"
        sess.commit()

        assert sc.version == 2

        ObjectExternalHistory = ObjectExternal.__history_mapper__.class_

        eq_(
            sess.query(ObjectExternalHistory).all(),
            [
                ObjectExternalHistory(
                    version=1, id1="aaa", id2="bbb", name="sc1"
                ),
            ],
        )

        sess.delete(sc)
        sess.commit()

        assert sess.query(ObjectExternal).count() == 0

        eq_(
            sess.query(ObjectExternalHistory).all(),
            [
                ObjectExternalHistory(
                    version=1, id1="aaa", id2="bbb", name="sc1"
                ),
                ObjectExternalHistory(
                    version=2, id1="aaa", id2="bbb", name="sc1modified"
                ),
            ],
        )

        sc = ObjectExternal(id1="aaa", id2="bbb", name="sc1reappeared")
        sess.add(sc)
        sess.commit()

        assert sc.version == 3

        sc.name = "sc1reappearedmodified"
        sess.commit()

        assert sc.version == 4

        eq_(
            sess.query(ObjectExternalHistory).all(),
            [
                ObjectExternalHistory(
                    version=1, id1="aaa", id2="bbb", name="sc1"
                ),
                ObjectExternalHistory(
                    version=2, id1="aaa", id2="bbb", name="sc1modified"
                ),
                ObjectExternalHistory(
                    version=3, id1="aaa", id2="bbb", name="sc1reappeared"
                ),
            ],
        )

class TestVersioningNewBase(TestVersioning):
    def make_base(self):
        class Base(DeclarativeBase):
            pass

        self.Base = Base

class TestVersioningUnittest(TestVersioning, unittest.TestCase):
    pass

class TestVersioningNewBaseUnittest(TestVersioningNewBase, unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_rows.versioned_map

```
"""A variant of the versioned_rows example built around the
concept of a "vertical table" structure, like those illustrated in
:ref:`examples_vertical_tables` examples.

Here we store a dictionary of key/value pairs, storing the k/v's in a
"vertical" fashion where each key gets a row. The value is split out
into two separate datatypes, string and int - the range of datatype
storage can be adjusted for individual needs.

Changes to the "data" attribute of a ConfigData object result in the
ConfigData object being copied into a new one, and new associations to
its data are created. Values which aren't changed between versions are
referenced by both the former and the newer ConfigData object.
Overall, only INSERT statements are emitted - no rows are UPDATed or
DELETEd.

An optional feature is also illustrated which associates individual
key/value pairs with the ConfigData object in which it first
originated. Since a new row is only persisted when a new value is
created for a particular key, the recipe provides a way to query among
the full series of changes which occurred for any particular key in
the dictionary.

The set of all ConfigData in a particular table represents a single
series of versions. By adding additional columns to ConfigData, the
system can be made to store multiple version streams distinguished by
those additional values.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import attributes
from sqlalchemy.orm import backref
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates
from sqlalchemy.orm.collections import attribute_keyed_dict

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    """Apply the new_version() method of objects which are
    marked as dirty during a flush.

    """
    for instance in session.dirty:
        if hasattr(instance, "new_version") and session.is_modified(instance):
            # make it transient
            instance.new_version(session)

            # re-add
            session.add(instance)

Base = declarative_base()

class ConfigData(Base):
    """Represent a series of key/value pairs.

    ConfigData will generate a new version of itself
    upon change.

    The "data" dictionary provides access via
    string name mapped to a string/int value.

    """

    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    """Primary key column of this ConfigData."""

    elements = relationship(
        "ConfigValueAssociation",
        collection_class=attribute_keyed_dict("name"),
        backref=backref("config_data"),
        lazy="subquery",
    )
    """Dictionary-backed collection of ConfigValueAssociation objects,
    keyed to the name of the associated ConfigValue.

    Note there's no "cascade" here.  ConfigValueAssociation objects
    are never deleted or changed.
    """

    def _new_value(name, value):
        """Create a new entry for usage in the 'elements' dictionary."""
        return ConfigValueAssociation(ConfigValue(name, value))

    data = association_proxy("elements", "value", creator=_new_value)
    """Proxy to the 'value' elements of each related ConfigValue,
    via the 'elements' dictionary.
    """

    def __init__(self, data):
        self.data = data

    @validates("elements")
    def _associate_with_element(self, key, element):
        """Associate incoming ConfigValues with this
        ConfigData, if not already associated.

        This is an optional feature which allows
        more comprehensive history tracking.

        """
        if element.config_value.originating_config is None:
            element.config_value.originating_config = self
        return element

    def new_version(self, session):
        # convert to an INSERT
        make_transient(self)
        self.id = None

        # history of the 'elements' collection.
        # this is a tuple of groups: (added, unchanged, deleted)
        hist = attributes.get_history(self, "elements")

        # rewrite the 'elements' collection
        # from scratch, removing all history
        attributes.set_committed_value(self, "elements", {})

        # new elements in the "added" group
        # are moved to our new collection.
        for elem in hist.added:
            self.elements[elem.name] = elem

        # copy elements in the 'unchanged' group.
        # the new ones associate with the new ConfigData,
        # the old ones stay associated with the old ConfigData
        for elem in hist.unchanged:
            self.elements[elem.name] = ConfigValueAssociation(
                elem.config_value
            )

        # we also need to expire changes on each ConfigValueAssociation
        # that is to remain associated with the old ConfigData.
        # Here, each one takes care of that in its new_version()
        # method, though we could do that here as well.

class ConfigValueAssociation(Base):
    """Relate ConfigData objects to associated ConfigValue objects."""

    __tablename__ = "config_value_association"

    config_id = Column(ForeignKey("config.id"), primary_key=True)
    """Reference the primary key of the ConfigData object."""

    config_value_id = Column(ForeignKey("config_value.id"), primary_key=True)
    """Reference the primary key of the ConfigValue object."""

    config_value = relationship("ConfigValue", lazy="joined", innerjoin=True)
    """Reference the related ConfigValue object."""

    def __init__(self, config_value):
        self.config_value = config_value

    def new_version(self, session):
        """Expire all pending state, as ConfigValueAssociation is immutable."""

        session.expire(self)

    @property
    def name(self):
        return self.config_value.name

    @property
    def value(self):
        return self.config_value.value

    @value.setter
    def value(self, value):
        """Intercept set events.

        Create a new ConfigValueAssociation upon change,
        replacing this one in the parent ConfigData's dictionary.

        If no net change, do nothing.

        """
        if value != self.config_value.value:
            self.config_data.elements[self.name] = ConfigValueAssociation(
                ConfigValue(self.config_value.name, value)
            )

class ConfigValue(Base):
    """Represent an individual key/value pair at a given point in time.

    ConfigValue is immutable.

    """

    __tablename__ = "config_value"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    originating_config_id = Column(
        Integer, ForeignKey("config.id"), nullable=False
    )
    int_value = Column(Integer)
    string_value = Column(String(255))

    def __init__(self, name, value):
        self.name = name
        self.value = value

    originating_config = relationship("ConfigData")
    """Reference to the originating ConfigData.

    This is optional, and allows history tracking of
    individual values.

    """

    def new_version(self, session):
        raise NotImplementedError("ConfigValue is immutable.")

    @property
    def value(self):
        for k in ("int_value", "string_value"):
            v = getattr(self, k)
            if v is not None:
                return v
        else:
            return None

    @value.setter
    def value(self, value):
        if isinstance(value, int):
            self.int_value = value
            self.string_value = None
        else:
            self.string_value = str(value)
            self.int_value = None

if __name__ == "__main__":
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    sess = Session()

    config = ConfigData(
        {"user_name": "twitter", "hash_id": "4fedffca37eaf", "x": 27, "y": 450}
    )

    sess.add(config)
    sess.commit()
    version_one = config.id

    config.data["user_name"] = "yahoo"
    sess.commit()

    version_two = config.id

    assert version_one != version_two

    # two versions have been created.

    assert config.data == {
        "user_name": "yahoo",
        "hash_id": "4fedffca37eaf",
        "x": 27,
        "y": 450,
    }

    old_config = sess.query(ConfigData).get(version_one)
    assert old_config.data == {
        "user_name": "twitter",
        "hash_id": "4fedffca37eaf",
        "x": 27,
        "y": 450,
    }

    # the history of any key can be acquired using
    # the originating_config_id attribute
    history = (
        sess.query(ConfigValue)
        .filter(ConfigValue.name == "user_name")
        .order_by(ConfigValue.originating_config_id)
        .all()
    )

    assert [(h.value, h.originating_config_id) for h in history] == (
        [("twitter", version_one), ("yahoo", version_two)]
    )
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_rows.versioned_rows

```
"""Illustrates a method to intercept changes on objects, turning
an UPDATE statement on a single row into an INSERT statement, so that a new
row is inserted with the new data, keeping the old row intact.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import attributes
from sqlalchemy.orm import backref
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

class Versioned:
    def new_version(self, session):
        # make us transient (removes persistent
        # identity).
        make_transient(self)

        # set 'id' to None.
        # a new PK will be generated on INSERT.
        self.id = None

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    for instance in session.dirty:
        if not isinstance(instance, Versioned):
            continue
        if not session.is_modified(instance):
            continue

        if not attributes.instance_state(instance).has_identity:
            continue

        # make it transient
        instance.new_version(session)
        # re-add
        session.add(instance)

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)

Session = sessionmaker(engine)

# example 1, simple versioning

class Example(Versioned, Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)
    data = Column(String)

Base.metadata.create_all(engine)

session = Session()
e1 = Example(data="e1")
session.add(e1)
session.commit()

e1.data = "e2"
session.commit()

assert session.query(Example.id, Example.data).order_by(Example.id).all() == (
    [(1, "e1"), (2, "e2")]
)

# example 2, versioning with a parent

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("child.id"))
    child = relationship("Child", backref=backref("parent", uselist=False))

class Child(Versioned, Base):
    __tablename__ = "child"

    id = Column(Integer, primary_key=True)
    data = Column(String)

    def new_version(self, session):
        # expire parent's reference to us
        session.expire(self.parent, ["child"])

        # create new version
        Versioned.new_version(self, session)

        # re-add ourselves to the parent
        self.parent.child = self

Base.metadata.create_all(engine)

session = Session()

p1 = Parent(child=Child(data="c1"))
session.add(p1)
session.commit()

p1.child.data = "c2"
session.commit()

assert p1.child_id == 2
assert session.query(Child.id, Child.data).order_by(Child.id).all() == (
    [(1, "c1"), (2, "c2")]
)
```
