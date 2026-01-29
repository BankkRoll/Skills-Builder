# Drizzle ORM

# Drizzle ORM

> Drizzle ORM is a lightweight and performant TypeScript ORM with developer experience in mind.

# Drizzle ORM

Drizzle ORM is a headless TypeScript ORM with a head. 🐲

> Drizzle is a good friend who’s there for you when necessary and doesn’t bother when you need some space.

It looks and feels simple, performs on day *1000* of your project,

lets you do things your way, and is there when you need it.

**It’s the only ORM with bothrelationalandSQL-likequery APIs**,
providing you the best of both worlds when it comes to accessing your relational data.
Drizzle is lightweight, performant, typesafe, non-lactose, gluten-free, sober, flexible and **serverless-ready by design**.
Drizzle is not just a library, it’s an experience. 🤩

## Headless ORM?

First and foremost, Drizzle is a library and a collection of complementary opt-in tools.

**ORM** stands for *object relational mapping*, and developers tend to call Django-like or Spring-like tools an ORM.
We truly believe it’s a misconception based on legacy nomenclature, and we call them **data frameworks**.

 WARNING

With data frameworks you have to build projects **around them** and not **with them**.

**Drizzle** lets you build your project the way you want, without interfering with your project or structure.

Using Drizzle you can define and manage database schemas in TypeScript, access your data in a SQL-like
or relational way, and take advantage of opt-in tools
to push your developer experience *through the roof*. 🤯

## Why SQL-like?

**If you know SQL, you know Drizzle.**

Other ORMs and data frameworks tend to deviate/abstract you away from SQL, which
leads to a double learning curve: needing to know both SQL and the framework’s API.

Drizzle is the opposite.
We embrace SQL and built Drizzle to be SQL-like at its core, so you can have zero to no
learning curve and access to the full power of SQL.

We bring all the familiar **SQL schema**, **queries**,
**automatic migrations** and **one more thing**. ✨

   index.tsschema.tsmigration.sql

```
// Access your data
await db
	.select()
	.from(countries)
	.leftJoin(cities, eq(cities.countryId, countries.id))
	.where(eq(countries.id, 10))
```

```
// manage your schema
export const countries = pgTable('countries', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 256 }),
});

export const cities = pgTable('cities', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 256 }),
  countryId: integer('country_id').references(() => countries.id),
});
```

```
-- generate migrations
CREATE TABLE IF NOT EXISTS "countries" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar(256)
);

CREATE TABLE IF NOT EXISTS "cities" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" varchar(256),
	"country_id" integer
);

ALTER TABLE "cities" ADD CONSTRAINT "cities_country_id_countries_id_fk" FOREIGN KEY ("country_id") REFERENCES "countries"("id") ON DELETE no action ON UPDATE no action;
```

## Why not SQL-like?

We’re always striving for a perfectly balanced solution, and while SQL-like does cover 100% of the needs,
there are certain common scenarios where you can query data in a better way.

We’ve built the **Queries API** for you, so you can fetch relational nested data from the database
in the most convenient and performant way, and never think about joins and data mapping.

**Drizzle always outputs exactly 1 SQL query.** Feel free to use it with serverless databases and never worry about performance or roundtrip costs!

```
const result = await db.query.users.findMany({
	with: {
		posts: true
	},
});
```

## Serverless?

The best part is no part. **Drizzle has exactly 0 dependencies!**

![Drizzle is slim an Serverless ready](https://orm.drizzle.team/_astro/drizzle31kb.6Mn-oJyX_ZHNm12.webp)

Drizzle ORM is dialect-specific, slim, performant and serverless-ready **by design**.

We’ve spent a lot of time to make sure you have best-in-class SQL dialect support, including Postgres, MySQL, and others.

Drizzle operates natively through industry-standard database drivers. We support all major **PostgreSQL**, **MySQL**, **SQLite** or **SingleStore** drivers out there, and we’re adding new ones **really fast**.

## Welcome on board!

More and more companies are adopting Drizzle in production, experiencing immense benefits in both DX and performance.

**We’re always there to help, so don’t hesitate to reach out. We’ll gladly assist you in your Drizzle journey!**

We have an outstanding **Discord community** and welcome all builders to our **Twitter**.

Now go build something awesome with Drizzle and your **PostgreSQL**, **MySQL** or **SQLite** database. 🚀

### Video Showcase

    [1:37:39Full Drizzle Course for BeginnersCode Genix](https://driz.link/yt/vyU5mJGCJMw)  [56:09Learn Drizzle In 60 MinutesWeb Dev Simplified](https://driz.link/yt/7-NZ0MlPpJA)  [2:55Drizzle ORM in 100 SecondsFireship](https://driz.link/yt/i_mAHOhpBSA)  [14:00Learn Drizzle ORM in 13 mins (crash course)Neon](https://driz.link/yt/hIYNOiZXQ7Y)  [38:08Easiest Database Setup in Next.js 14 with Turso & DrizzleSam Meech-Ward](https://driz.link/yt/4ZhtoOFKFP8)  [5:46:28Next.js Project with Vercel, Neon, Drizzle, TailwindCSS, FlowBite and more!CodingEntrepreneurs](https://driz.link/yt/NfVELsEZFsA)  [5:46I Have A New Favorite Database ToolTheo - t3.gg](https://driz.link/yt/_SLxGYzv6jo)  [33:52Drizzle ORM First impressions - migrations, relations, queries!Marius Espejo](https://driz.link/yt/Qo-RXkSwOtc)  [9:00I want to learn Drizzle ORM, so I'm starting another next14 projectWeb Dev Cody](https://driz.link/yt/yXNEqyvA0OY)  [5:18Picking an ORM is Getting Harder...Ben Davis](https://driz.link/yt/h7vVhR-dFYo)  [8:49This New Database Tool is a Game-ChangerJosh tried coding](https://driz.link/yt/8met6WTk0mQ)  [4:23My Favorite Database Tool Just Got EVEN BetterJosh tried coding](https://driz.link/yt/woWW1T9DXEY)  [11:41:46SaaS Notion Clone with Realtime cursors, Nextjs 13, Stripe, Drizzle ORM, Tailwind, Supabase, SocketsWeb Prodigies](https://driz.link/yt/A3l6YYkXzzg)  [12:18SvelteKit + Drizzle Code BreakdownBen Davis](https://driz.link/yt/EQfaw5bDE1s)  [2:01:29Build a Multi-Tenanted, Role-Based Access Control SystemTomDoesTech](https://driz.link/yt/b6VhN_HHDiQ)  [5:42The Prisma killer is finally hereSST](https://driz.link/yt/3tl9XCiQErA)  [1:07:41Learning Drizzle ORM and working on a next14 projectWeb Dev Cody](https://driz.link/yt/VQFjyEa8vGE)  [6:01This Trick Makes My Favorite Database Tool Even BetterJosh tried coding](https://driz.link/yt/5G0upg4sxgE)  [26:29Effortless Auth in Next.js 14: Use Auth.js & Drizzle ORM for Secure LoginSam Meech-Ward](https://driz.link/yt/-JnEuvPmt-Q)      <Footer />
