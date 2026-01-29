# Request Parameters¶

# Request Parameters¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Request Parameters¶

Here's the reference information for the request parameters.

These are the special functions that you can put in *path operation function* parameters or dependency functions with `Annotated` to get data from the request.

It includes:

- `Query()`
- `Path()`
- `Body()`
- `Cookie()`
- `Header()`
- `Form()`
- `File()`

You can import them all directly from `fastapi`:

```
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

## fastapi.Query¶

```
Query(
    default=Undefined,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456457458459460461462463464465466467468469470471472473474475476477478479480481482483484485486487488489490491492493494495496497498499500501502503504505506507508509510511512513514515516517518519520521522523524525526527528529530531532533534535536537538539540541542543544545546547548549550551552553554555556557558559560561562563564565566567568569570571572573574575576577578579580581582583584585586587588589590591592593594595596597598599600601602603604605606607608609610611612613614615616617618619620621622623624625626627628629630631632633634635636637638639 | defQuery(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.Query(default=default,default_factory=default_factory,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.Path¶

```
Path(
    default=...,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

Declare a path parameter for a *path operation*.

Read more about it in the
[FastAPI docs for Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/).

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
):
    return {"item_id": item_id}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:AnyDEFAULT:... |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 1415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337 | defPath(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=...,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:"""Declare a path parameter for a *path operation*.Read more about it in the[FastAPI docs for Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/).```pythonfrom typing import Annotatedfrom fastapi import FastAPI, Pathapp = FastAPI()@app.get("/items/{item_id}")async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")],):return {"item_id": item_id}```"""returnparams.Path(default=default,default_factory=default_factory,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.Body¶

```
Body(
    default=Undefined,
    *,
    default_factory=_Unset,
    embed=None,
    media_type="application/json",
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| embed | WhenembedisTrue, the parameter will be expected in a JSON body as a
key instead of being the JSON body itself.This happens automatically when more than oneBodyparameter is declared.Read more about it in theFastAPI docs for Body - Multiple Parameters.TYPE:Union[bool, None]DEFAULT:None |
| media_type | The media type of this parameter field. Changing it would affect the
generated OpenAPI, but currently it doesn't affect the parsing of the data.TYPE:strDEFAULT:'application/json' |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 1258125912601261126212631264126512661267126812691270127112721273127412751276127712781279128012811282128312841285128612871288128912901291129212931294129512961297129812991300130113021303130413051306130713081309131013111312131313141315131613171318131913201321132213231324132513261327132813291330133113321333133413351336133713381339134013411342134313441345134613471348134913501351135213531354135513561357135813591360136113621363136413651366136713681369137013711372137313741375137613771378137913801381138213831384138513861387138813891390139113921393139413951396139713981399140014011402140314041405140614071408140914101411141214131414141514161417141814191420142114221423142414251426142714281429143014311432143314341435143614371438143914401441144214431444144514461447144814491450145114521453145414551456145714581459146014611462146314641465146614671468146914701471147214731474147514761477147814791480148114821483148414851486148714881489149014911492149314941495149614971498149915001501150215031504150515061507150815091510151115121513151415151516151715181519152015211522152315241525152615271528152915301531153215331534153515361537153815391540154115421543154415451546154715481549155015511552155315541555155615571558155915601561156215631564156515661567156815691570157115721573157415751576157715781579158015811582 | defBody(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,embed:Annotated[Union[bool,None],Doc("""When `embed` is `True`, the parameter will be expected in a JSON body as akey instead of being the JSON body itself.This happens automatically when more than one `Body` parameter is declared.Read more about it in the[FastAPI docs for Body - Multiple Parameters](https://fastapi.tiangolo.com/tutorial/body-multiple-params/#embed-a-single-body-parameter)."""),]=None,media_type:Annotated[str,Doc("""The media type of this parameter field. Changing it would affect thegenerated OpenAPI, but currently it doesn't affect the parsing of the data."""),]="application/json",alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.Body(default=default,default_factory=default_factory,embed=embed,media_type=media_type,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.Cookie¶

```
Cookie(
    default=Undefined,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 9569579589599609619629639649659669679689699709719729739749759769779789799809819829839849859869879889899909919929939949959969979989991000100110021003100410051006100710081009101010111012101310141015101610171018101910201021102210231024102510261027102810291030103110321033103410351036103710381039104010411042104310441045104610471048104910501051105210531054105510561057105810591060106110621063106410651066106710681069107010711072107310741075107610771078107910801081108210831084108510861087108810891090109110921093109410951096109710981099110011011102110311041105110611071108110911101111111211131114111511161117111811191120112111221123112411251126112711281129113011311132113311341135113611371138113911401141114211431144114511461147114811491150115111521153115411551156115711581159116011611162116311641165116611671168116911701171117211731174117511761177117811791180118111821183118411851186118711881189119011911192119311941195119611971198119912001201120212031204120512061207120812091210121112121213121412151216121712181219122012211222122312241225122612271228122912301231123212331234123512361237123812391240124112421243124412451246124712481249125012511252125312541255 | defCookie(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.Cookie(default=default,default_factory=default_factory,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.Header¶

```
Header(
    default=Undefined,
    *,
    default_factory=_Unset,
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    convert_underscores=True,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| convert_underscores | Automatically convert underscores to hyphens in the parameter field name.Read more about it in theFastAPI docs for Header ParametersTYPE:boolDEFAULT:True |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 642643644645646647648649650651652653654655656657658659660661662663664665666667668669670671672673674675676677678679680681682683684685686687688689690691692693694695696697698699700701702703704705706707708709710711712713714715716717718719720721722723724725726727728729730731732733734735736737738739740741742743744745746747748749750751752753754755756757758759760761762763764765766767768769770771772773774775776777778779780781782783784785786787788789790791792793794795796797798799800801802803804805806807808809810811812813814815816817818819820821822823824825826827828829830831832833834835836837838839840841842843844845846847848849850851852853854855856857858859860861862863864865866867868869870871872873874875876877878879880881882883884885886887888889890891892893894895896897898899900901902903904905906907908909910911912913914915916917918919920921922923924925926927928929930931932933934935936937938939940941942943944945946947948949950951952953 | defHeader(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,convert_underscores:Annotated[bool,Doc("""Automatically convert underscores to hyphens in the parameter field name.Read more about it in the[FastAPI docs for Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/#automatic-conversion)"""),]=True,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.Header(default=default,default_factory=default_factory,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,convert_underscores=convert_underscores,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.Form¶

```
Form(
    default=Undefined,
    *,
    default_factory=_Unset,
    media_type="application/x-www-form-urlencoded",
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| media_type | The media type of this parameter field. Changing it would affect the
generated OpenAPI, but currently it doesn't affect the parsing of the data.TYPE:strDEFAULT:'application/x-www-form-urlencoded' |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 1585158615871588158915901591159215931594159515961597159815991600160116021603160416051606160716081609161016111612161316141615161616171618161916201621162216231624162516261627162816291630163116321633163416351636163716381639164016411642164316441645164616471648164916501651165216531654165516561657165816591660166116621663166416651666166716681669167016711672167316741675167616771678167916801681168216831684168516861687168816891690169116921693169416951696169716981699170017011702170317041705170617071708170917101711171217131714171517161717171817191720172117221723172417251726172717281729173017311732173317341735173617371738173917401741174217431744174517461747174817491750175117521753175417551756175717581759176017611762176317641765176617671768176917701771177217731774177517761777177817791780178117821783178417851786178717881789179017911792179317941795179617971798179918001801180218031804180518061807180818091810181118121813181418151816181718181819182018211822182318241825182618271828182918301831183218331834183518361837183818391840184118421843184418451846184718481849185018511852185318541855185618571858185918601861186218631864186518661867186818691870187118721873187418751876187718781879188018811882188318841885188618871888188918901891189218931894 | defForm(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,media_type:Annotated[str,Doc("""The media type of this parameter field. Changing it would affect thegenerated OpenAPI, but currently it doesn't affect the parsing of the data."""),]="application/x-www-form-urlencoded",alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.Form(default=default,default_factory=default_factory,media_type=media_type,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |

## fastapi.File¶

```
File(
    default=Undefined,
    *,
    default_factory=_Unset,
    media_type="multipart/form-data",
    alias=None,
    alias_priority=_Unset,
    validation_alias=None,
    serialization_alias=None,
    title=None,
    description=None,
    gt=None,
    ge=None,
    lt=None,
    le=None,
    min_length=None,
    max_length=None,
    pattern=None,
    regex=None,
    discriminator=None,
    strict=_Unset,
    multiple_of=_Unset,
    allow_inf_nan=_Unset,
    max_digits=_Unset,
    decimal_places=_Unset,
    examples=None,
    example=_Unset,
    openapi_examples=None,
    deprecated=None,
    include_in_schema=True,
    json_schema_extra=None,
    **extra
)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| default | Default value if the parameter field is not set.TYPE:AnyDEFAULT:Undefined |
| default_factory | A callable to generate the default value.This doesn't affectPathparameters as the value is always required.
The parameter is available only for compatibility.TYPE:Union[Callable[[],Any], None]DEFAULT:_Unset |
| media_type | The media type of this parameter field. Changing it would affect the
generated OpenAPI, but currently it doesn't affect the parsing of the data.TYPE:strDEFAULT:'multipart/form-data' |
| alias | An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.
It is particularly useful when you can't use the name you want because it
is a Python reserved keyword or similar.TYPE:Optional[str]DEFAULT:None |
| alias_priority | Priority of the alias. This affects whether an alias generator is used.TYPE:Union[int, None]DEFAULT:_Unset |
| validation_alias | 'Whitelist' validation step. The parameter field will be the single one
allowed by the alias or set of aliases defined.TYPE:Union[str,AliasPath,AliasChoices, None]DEFAULT:None |
| serialization_alias | 'Blacklist' validation step. The vanilla parameter field will be the
single one of the alias' or set of aliases' fields and all the other
fields will be ignored at serialization time.TYPE:Union[str, None]DEFAULT:None |
| title | Human-readable title.TYPE:Optional[str]DEFAULT:None |
| description | Human-readable description.TYPE:Optional[str]DEFAULT:None |
| gt | Greater than. If set, value must be greater than this. Only applicable to
numbers.TYPE:Optional[float]DEFAULT:None |
| ge | Greater than or equal. If set, value must be greater than or equal to
this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| lt | Less than. If set, value must be less than this. Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| le | Less than or equal. If set, value must be less than or equal to this.
Only applicable to numbers.TYPE:Optional[float]DEFAULT:None |
| min_length | Minimum length for strings.TYPE:Optional[int]DEFAULT:None |
| max_length | Maximum length for strings.TYPE:Optional[int]DEFAULT:None |
| pattern | RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| regex | Deprecated in FastAPI 0.100.0 and Pydantic v2, usepatterninstead. RegEx pattern for strings.TYPE:Optional[str]DEFAULT:None |
| discriminator | Parameter field name for discriminating the type in a tagged union.TYPE:Union[str, None]DEFAULT:None |
| strict | IfTrue, strict validation is applied to the field.TYPE:Union[bool, None]DEFAULT:_Unset |
| multiple_of | Value must be a multiple of this. Only applicable to numbers.TYPE:Union[float, None]DEFAULT:_Unset |
| allow_inf_nan | Allowinf,-inf,nan. Only applicable to numbers.TYPE:Union[bool, None]DEFAULT:_Unset |
| max_digits | Maximum number of allow digits for strings.TYPE:Union[int, None]DEFAULT:_Unset |
| decimal_places | Maximum number of decimal places allowed for numbers.TYPE:Union[int, None]DEFAULT:_Unset |
| examples | Example values for this field.TYPE:Optional[list[Any]]DEFAULT:None |
| example | Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.TYPE:Optional[Any]DEFAULT:_Unset |
| openapi_examples | OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at/docs).Swagger UI (that provides the/docsinterface) has better support for the
OpenAPI-specific examples than the JSON Schemaexamples, that's the main
use case for this.Read more about it in theFastAPI docs for Declare Request Example Data.TYPE:Optional[dict[str,Example]]DEFAULT:None |
| deprecated | Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at/docs).TYPE:Union[deprecated,str,bool, None]DEFAULT:None |
| include_in_schema | To include (or not) this parameter field in the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| json_schema_extra | Any additional JSON schema data.TYPE:Union[dict[str,Any], None]DEFAULT:None |
| **extra | Theextrakwargs is deprecated. Usejson_schema_extrainstead. Include extra fields used by the JSON Schema.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/param_functions.py`

| 1897189818991900190119021903190419051906190719081909191019111912191319141915191619171918191919201921192219231924192519261927192819291930193119321933193419351936193719381939194019411942194319441945194619471948194919501951195219531954195519561957195819591960196119621963196419651966196719681969197019711972197319741975197619771978197919801981198219831984198519861987198819891990199119921993199419951996199719981999200020012002200320042005200620072008200920102011201220132014201520162017201820192020202120222023202420252026202720282029203020312032203320342035203620372038203920402041204220432044204520462047204820492050205120522053205420552056205720582059206020612062206320642065206620672068206920702071207220732074207520762077207820792080208120822083208420852086208720882089209020912092209320942095209620972098209921002101210221032104210521062107210821092110211121122113211421152116211721182119212021212122212321242125212621272128212921302131213221332134213521362137213821392140214121422143214421452146214721482149215021512152215321542155215621572158215921602161216221632164216521662167216821692170217121722173217421752176217721782179218021812182218321842185218621872188218921902191219221932194219521962197219821992200220122022203220422052206 | defFile(# noqa: N802default:Annotated[Any,Doc("""Default value if the parameter field is not set."""),]=Undefined,*,default_factory:Annotated[Union[Callable[[],Any],None],Doc("""A callable to generate the default value.This doesn't affect `Path` parameters as the value is always required.The parameter is available only for compatibility."""),]=_Unset,media_type:Annotated[str,Doc("""The media type of this parameter field. Changing it would affect thegenerated OpenAPI, but currently it doesn't affect the parsing of the data."""),]="multipart/form-data",alias:Annotated[Optional[str],Doc("""An alternative name for the parameter field.This will be used to extract the data and for the generated OpenAPI.It is particularly useful when you can't use the name you want because itis a Python reserved keyword or similar."""),]=None,alias_priority:Annotated[Union[int,None],Doc("""Priority of the alias. This affects whether an alias generator is used."""),]=_Unset,validation_alias:Annotated[Union[str,AliasPath,AliasChoices,None],Doc("""'Whitelist' validation step. The parameter field will be the single oneallowed by the alias or set of aliases defined."""),]=None,serialization_alias:Annotated[Union[str,None],Doc("""'Blacklist' validation step. The vanilla parameter field will be thesingle one of the alias' or set of aliases' fields and all the otherfields will be ignored at serialization time."""),]=None,title:Annotated[Optional[str],Doc("""Human-readable title."""),]=None,description:Annotated[Optional[str],Doc("""Human-readable description."""),]=None,gt:Annotated[Optional[float],Doc("""Greater than. If set, value must be greater than this. Only applicable tonumbers."""),]=None,ge:Annotated[Optional[float],Doc("""Greater than or equal. If set, value must be greater than or equal tothis. Only applicable to numbers."""),]=None,lt:Annotated[Optional[float],Doc("""Less than. If set, value must be less than this. Only applicable to numbers."""),]=None,le:Annotated[Optional[float],Doc("""Less than or equal. If set, value must be less than or equal to this.Only applicable to numbers."""),]=None,min_length:Annotated[Optional[int],Doc("""Minimum length for strings."""),]=None,max_length:Annotated[Optional[int],Doc("""Maximum length for strings."""),]=None,pattern:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),]=None,regex:Annotated[Optional[str],Doc("""RegEx pattern for strings."""),deprecated("Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."),]=None,discriminator:Annotated[Union[str,None],Doc("""Parameter field name for discriminating the type in a tagged union."""),]=None,strict:Annotated[Union[bool,None],Doc("""If `True`, strict validation is applied to the field."""),]=_Unset,multiple_of:Annotated[Union[float,None],Doc("""Value must be a multiple of this. Only applicable to numbers."""),]=_Unset,allow_inf_nan:Annotated[Union[bool,None],Doc("""Allow `inf`, `-inf`, `nan`. Only applicable to numbers."""),]=_Unset,max_digits:Annotated[Union[int,None],Doc("""Maximum number of allow digits for strings."""),]=_Unset,decimal_places:Annotated[Union[int,None],Doc("""Maximum number of decimal places allowed for numbers."""),]=_Unset,examples:Annotated[Optional[list[Any]],Doc("""Example values for this field."""),]=None,example:Annotated[Optional[Any],deprecated("Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, ""although still supported. Use examples instead."),]=_Unset,openapi_examples:Annotated[Optional[dict[str,Example]],Doc("""OpenAPI-specific examples.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Swagger UI (that provides the `/docs` interface) has better support for theOpenAPI-specific examples than the JSON Schema `examples`, that's the mainuse case for this.Read more about it in the[FastAPI docs for Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#using-the-openapi_examples-parameter)."""),]=None,deprecated:Annotated[Union[deprecated,str,bool,None],Doc("""Mark this parameter field as deprecated.It will affect the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) this parameter field in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,json_schema_extra:Annotated[Union[dict[str,Any],None],Doc("""Any additional JSON schema data."""),]=None,**extra:Annotated[Any,Doc("""Include extra fields used by the JSON Schema."""),deprecated("""The `extra` kwargs is deprecated. Use `json_schema_extra` instead."""),],)->Any:returnparams.File(default=default,default_factory=default_factory,media_type=media_type,alias=alias,alias_priority=alias_priority,validation_alias=validation_alias,serialization_alias=serialization_alias,title=title,description=description,gt=gt,ge=ge,lt=lt,le=le,min_length=min_length,max_length=max_length,pattern=pattern,regex=regex,discriminator=discriminator,strict=strict,multiple_of=multiple_of,allow_inf_nan=allow_inf_nan,max_digits=max_digits,decimal_places=decimal_places,example=example,examples=examples,openapi_examples=openapi_examples,deprecated=deprecated,include_in_schema=include_in_schema,json_schema_extra=json_schema_extra,**extra,) |
| --- | --- |
