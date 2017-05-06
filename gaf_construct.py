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

TextAlignments = Enum(Int8ul,
    TEXT_ALIGNMENT_LEFT=0,
    TEXT_ALIGNMENT_RIGHT=1,
    TEXT_ALIGNMENT_CENTER=2,
    TEXT_ALIGNMENT_JUSTIFY=3,
    TEXT_ALIGNMENT_START=4,
    TEXT_ALIGNMENT_END=5,
)

tag_defs = Enum(Int16sl,
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

atl2_extras = Struct(
    "hasScale9Grid" / Flag, #atl2/3
    "scale9Grid" / If(this.hasScale9Grid, Rect), #atl2/3
)

atl3_extras = Struct(
    # these extras are also in atl2
    # Embedded() doesn't work inside Switch(), so we have to repeat.
    "hasScale9Grid" / Flag, #atl2/3
    "scale9Grid" / If(this.hasScale9Grid, Rect), #atl2/3
    # atl3 only
    "elScaleX" / Float32l, #atl3
    "elScaleY" / Float32l, #atl3
    "rotation" / Flag, #atl3
    "linkageName" / GAFString, #atl3
)

AtlasElement = Struct(
    "pivot" / Point,
    "topLeft" / Point,
    "elScale" / Switch(this._._.tag_type, {
        "TAG_DEFINE_ATLAS": Float32l,
        "TAG_DEFINE_ATLAS2": Float32l,
    }, default=None), #only on TAG_DEFINE_ATLAS and TAG_DEFINE_ATLAS2
    "elW" / Float32l,
    "elH" / Float32l,
    "atlID" / Int32ul,
    "elID" / Int32ul,
    Embedded(Switch(this._._.tag_type, {
        "TAG_DEFINE_ATLAS2": atl2_extras,
        "TAG_DEFINE_ATLAS3": atl3_extras,
    }, default=None)),
    "probe" / Probe(),
)

AtlasSource = Struct(
    "alId" / Int32ul,
    "slCount" / Int8ul,
    "sourceInfo" / Array(this.slCount, Struct(
        "source" / GAFString,
        "contentScale" / Float32l,
    )),
)

atlas = Struct(
    "displayScale" / Float32l,
    "alCount" / Int8ul,
    "alSources" / AtlasSource[this.alCount],
    "elCount" / Int32ul,
    "elContent" / AtlasElement[this.elCount]
)

blurFilter = Struct(
    "blurX" / Float32l,
    "blurY" / Float32l,
)

glowFilter = Struct(
    "color" / Int32ul,
    "blurX" / Float32l,
    "blurY" / Float32l,
    "strength" / Float32l,
    "inner" / Flag,
    "knockout" / Flag,
)

colorMatrixFilter = Struct(
    "matrix" / Float32l[20]
)

animationMasks = Struct(
    "maskLength" / Int32ul,
    "masks" / Array(this.maskLength, Struct(
        "objectId" / Int32ul,
        "regionId" / Int32ul,
        "type" / Switch(this._.tag_type, {
            'TAG_DEFINE_ANIMATION_MASKS': 0,
        }, default=Int8ul),
    )
)
)

animationObjects = Struct(
    "objectLength" / Int32ul,
    "objects" / Array(this.objectLength, Struct(
        "objectId" / Int32ul,
        "regionId" / Int32ul,
        "type" / Switch(this._.tag_type, {
            'TAG_DEFINE_ANIMATION_OBJECTS': 0,
        }, default=Int8ul),
    )
)
)

animationSequences = Struct(
    "sequenceLength" / Int32ul,
    "sequences" / Array(this.sequenceLength, Struct(
        "sequenceId" / GAFString,
        "startFrameNo" / Int16ul,
        "endFrameNo" / Int16ul,
    )
)
)

dropShadowFilter = Struct(
    "color" / Int32ul,
    "blurX" / Float32l,
    "blurY" / Float32l,
    "angle" / Float32l,
    "distance" / Float32l,
    "strength" / Float32l,
    "inner" / Flag,
    "knockout" / Flag,
)

namedParts = Struct(
    "length" / Int32ul,
    "parts" / Array(this.length, Struct(
        "partId" / Int32ul,
        "name" / GAFString,
    )
    )
)

sound = Struct(
    "soundCount" / Int16ul,
    "sounds" / Array(this.soundCount, Struct(
    "id" / Int16ul,
    "linkage" / GAFString,
    "source" / GAFString,
    "format" / Int8ul,
    "rate" / Int8ul,
    "sampleSize" / Int8ul,
    "stereo" / Flag,
    "sampleCount" / Int32ul,
    )
    )
)

textFields = Struct(
    "textFieldCount" / Int32ul,
    "Fields" / Array(this.textFieldCount, Struct(
    "textFieldID" / Int32ul,
    "pivotX" / Float32l,
    "pivotY" / Float32l,
    "width" / Float32l,
    "height" / Float32l,
    "text" / GAFString,
    "embedFonts" / Flag,
    "multiline" / Flag,
    "wordWrap" / Flag,
    "hasRestrict" / Flag,
    "restric" / If(self.hasRestrict, GAFString),
    "editable" / Flag,
    "selectable" / Flag,
    "displayAsPassword" / Flag,
    "maxChars" / Int32ul,
    "alignFlag" / Int32ul,
    "blockIndent" / Int32ul,
    "bold" / Flag,
    "bullet" / Flag,
    "color" / Int32ul,
    "font" / GAFString,
    "indent" / Int32ul,
    "italic" / Flag,
    "kerning" / Flag,
    "leading" / Int32ul,
    "leftMargin" / Int32ul,
    "letterSpacing" / Float32l,
    "rightMargin" / Int32ul,
    "size" / Int32ul,
    "tabStopCount" / Int32ul,
    "tabStops" / Int32ul[this.tabStopCount],
    "target" / GAFString,
    "underline" / Flag,
    "url" / GAFString,
    "align" / TextAlignments,
    ))
)


tags = Struct(
    "tag_type" / tag_defs,
    #"p" / Probe(),
    "length" / Int32ul,
    "detail" / Switch(this.tag_type,
      {
        "TAG_DEFINE_STAGE": stage_def,
        "TAG_DEFINE_TIMELINE": timeline_def,
        "TAG_DEFINE_ATLAS3": atlas,
        "TAG_DEFINE_ATLAS2": atlas,
        "TAG_DEFINE_ATLAS": atlas,
        "TAG_DEFINE_ANIMATION_MASKS": animationMasks,
        "TAG_DEFINE_ANIMATION_MASKS2": animationMasks,
        "TAG_DEFINE_ANIMATION_OBJECTS": animationObjects,
        "TAG_DEFINE_ANIMATION_OBJECTS2": animationObjects,
        "TAG_DEFINE_ANIMATION_FRAMES": animationFrames,
        "TAG_DEFINE_ANIMATION_FRAMES2": animationFrames,
        "TAG_DEFINE_NAMED_PARTS": namedParts,
        "TAG_DEFINE_SEQUENCES": sequences,
        "TAG_DEFINE_SEQUENCES": sounds,
        "TAG_DEFINE_TEXT_FIELDS": textFields,
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
    "tags" / tags[:],
)
