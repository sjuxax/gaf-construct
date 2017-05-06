from construct import *

gaf_header_compressed = Struct(
    "sig" / Const(b"CAG"),
)

gaf_header_std = Struct(
    "sig" / Const(b"FAG\x00"),
)

gaf_version = Struct(
    "versionMinor" / Int8ul,
    "versionMajor" / Int8ul,
)

gaf_display_scale = Struct(
    "count" / Int32ul,
    "values" / Array(this.count, Float32l),
)

gaf_content_scale = Struct(
    "count" / Int32ul,
    "values" / Array(this.count, Float32l),
)


tag_type = Enum(Int16sl,
    TAG_END=0,
    TAG_DEFINE_ATLAS=1,
    TAG_DEFINE_ANIMATION_MASKS=2,
    TAG_DEFINE_ANIMATION_OBJECTS=3,
    TAG_DEFINE_ANIMATION_FRAMES=4,
    TAG_DEFINE_NAMED_PARTS=5,
    TAG_DEFINE_SEQUENCES=6,
    TAG_DEFINE_TEXT_FIELDS=7, # v4.0
    TAG_DEFINE_ATLAS2=8, # v4.0
    TAG_DEFINE_STAGE=9,
    TAG_DEFINE_ANIMATION_OBJECTS2=10, # v4.0
    TAG_DEFINE_ANIMATION_MASKS2=11, # v4.0
    TAG_DEFINE_ANIMATION_FRAMES2=12, # v4.0
    TAG_DEFINE_TIMELINE=13, # v4.0
    TAG_DEFINE_SOUNDS=14, # v5.0
    TAG_DEFINE_ATLAS3=15, # v5.0
)


stage_def = Struct(
    "probe" / Probe(),
    "fps" /  Int8ul,
    "color" / Int32sl,
    "width" / Int16ul,
    "height" / Int16ul,
)

Rect = Array(4, Float32l)
Point = Array(2, Float32l)
GAFString = PascalString(Int16ul, encoding='utf8')

timeline_def = Struct(
    "id" / Int32ul,
    "frameCount" / Int32ul,
    "bounds" / Rect,
    "pivot" / Point,
    "has_linkage" / Flag,
    "linkage_name" / IfThenElse(this.has_linkage,
                        GAFString,
                        "")
)

AtlasElement = Struct(
    "elMark" / Int32ul,
    "pivot" / Point,
    "topLeft" / Point,
    "elScale" / Float32l, #only on TAG_DEFINE_ATLAS and TAG_DEFINE_ATLAS2
    "elW" / Float32l,
    "elH" / Float32l,
    "atlID" / Int32ul,
    "elID" / Int32ul,
    "hasScale9Grid" / Flag, #atl2/3
    "scale9Grid" / If(this.hasScale9Grid, Rect), #atl2/3
    #"elScaleX" / Float32l, #atl3
    #"elScaleY" / Float32l, #atl3
    #"rotation" / Flag, #atl3
    #"linkageName" / GAFString, #atl3
)

AtlasSource = Struct(
    "slid" / Int8ul,
    "p" / Probe(),
    "source" / GAFString,
    "p" / ProbeInto(this.source),
    "contentScale" / Float32l,
    "elContent" / AtlasElement[:]
)

AtlasMember = Struct(
        "almark" / Int8ul,
        "alid" / Int32ul,
        "sl_member" / AtlasSource[:]
        )


atlas = Struct(
    "displayScale" / Float32l,
    "alMember" / AtlasMember[:],
)

tags = Struct(
    "id" / tag_type,
    "p" / Probe(),
    "length" / Int32ul,
    "detail" / Switch(this.id,
      {
        "TAG_DEFINE_STAGE": stage_def,
        "TAG_DEFINE_TIMELINE": timeline_def,
        "TAG_DEFINE_ATLAS3": atlas,
        "TAG_DEFINE_ATLAS2": atlas,
        "TAG_DEFINE_ATLAS": atlas,
        "TAG_END": "die."
      }
    )
)

gaf_file = Struct(
    "header" / gaf_header_std,
    "version" / gaf_version,
    "length" / Int32ul,
    "display_scale" / gaf_display_scale,
    "content_scale" / gaf_content_scale,
    "tags" / tags[4],
)
