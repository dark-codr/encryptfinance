CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        # 'skin': 'office2013',
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates",
                    "-",
                    "Preview",
                    "Maximize",
                    "ShowBlocks",
                ],
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "about", "items": ["About"]},
            "/",  # put this to force next toolbar on new line
            {
                "name": "yourcustomtools",
                "items": [
                    # put the name of your editor.ui.addButton here
                    "Magicline",
                    "Mathjax",
                    "Menubutton",
                    "Notification",
                    "Notificationaggregator",
                    "Youtube",
                ],
            },
        ],
        "toolbar": "YourCustomToolbarConfig",  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        "height": 191,
        "width": "100%",
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        "toolbarCanCollapse": True,
        "mathJaxLib": "//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                # 'codesnippet'
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "devtools",
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                # 'elementspath'
                "liststyle",
                "magicline",
                "mathjax",
                "menubutton",
                "notification",
                "notificationaggregator",
                "youtube",
            ]
        ),
    }
}
