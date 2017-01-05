from flask_assets import Bundle

def create_assets(assets):

    js = Bundle(
        'js/jquery-2.2.4.min.js',
        'js/bootstrap.js',
        'js/ripples.min.js',
        'js/material.min.js',
        filters='rjsmin',
        output='js/libs.js'
    )

    css = Bundle(
        'css/bootstrap.css',
        'css/ripples.css',
        'css/style.css',
        'css/bootstrap-material-design.css',
        'css/font-awesome.min.css',
        filters='cssmin',
        output='css/min.css'
    )

    datepickercss = Bundle(
        'css/bootstrap-material-datetimepicker.css',
        filters='cssmin',
        output='css/datapicker.css'
    )

    datepickerjs = Bundle(
        'js/moment.js',
        'js/bootstrap-material-datetime.js',
        filters='rjsmin',
        output='js/datapicker.js'
    )

    codemirrorcss = Bundle(
        'codemirror/lib/codemirror.css',
        'codemirror/lib/ttcn.css',
         filters='cssmin',
         output='css/cm.css'
    )

    codemirrorjs = Bundle(
        'codemirror/lib/codemirror.js',
        filters='rjsmin',
        output='js/cm.js'
    )


    codepretiffycss = Bundle(
        'google-code-prettify/prettify.css',
         filters='cssmin',
         output='css/prettify.css'
    )

    codecodepretiffyjs = Bundle(
        'google-code-prettify/run_prettify.js',
        filters='rjsmin',
        output='js/prettify.js'
    )


    assets.register('js_main', js)
    assets.register('css_main', css)

    assets.register('css_datapicker', datepickercss)
    assets.register('js_datapicker', datepickerjs)

    assets.register('css_cm', codemirrorcss)
    assets.register('js_cm', codemirrorjs)
    
    assets.register('css_pr', codepretiffycss)
    assets.register('js_pr', codecodepretiffyjs)