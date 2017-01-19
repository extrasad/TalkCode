function FormLanguage (config) {
    this.form = config.form;
    this.output = config.output;
    this.langs = [
        {
        "python-#62bd9b": "py",
        "javascript-#ffea72": "js",
        "coffeescript-#6f4e37": "coffee",
        "livescript-#499886": "ls",
        "typescript-#31859c": "typescript",
        "asp.net-#6a40fd": "aspx",
        "ada-##02f88c": "ada",
        "c-#555": "c",
        "cpp-#f34b7d": "cpp",
        "css-#563d7c": "css",
        "clojure s-#db5855": "cljs", 
        "clojure x-#db5855": "cljx", 
        "clojure c-#db5855": "cljc", 
        "clojure j-#db5855": "clj",
        "dart-#98BAD6": "dart",
        "common lisp-#3fb68b": "cl",
        "lisp-#3fb68b": "lisp",
        "common  lisp-#3fb68b": "el",
        "d-#fcd46d": "d",
        "eiffel-946d57": "e",
        "erlang-#0faf8d": "erl",
        "fortran-#4d41b1": "f90",
        "f#-#b845fc": "fs",
        "groovy-#e69f56": "groovy",
        "groovy gradle-#e69f56": "gradle",
        "java-#b07219": "java",
        "java server page-#b07219": "x-jsp",
        "json-#ffdd72": "json", 
        "lua-#fa1fa1": "lua",
        "sql-#aa2472": "sql",
        "objective c-#438eff": "mm",
        "pascal-#b0ce4e": "p",
        "php-#4F5D95": "php",
        "oz-#fcaf3e": "oz",
        "puppet-#cc5555": "pp",
        "r-#198ce7": "r",
        "ruby-#701516": "ruby",
        "rust-#dea584": "rust",
        "scala-#7dd3b0": "scala",
        "scss-#ffb6c1": "scss",
        "sass-#ffb6c1": "sass",
        "swift-#ffac45": "swift",
        "go-#375eab": "go",
        "haskell-#551a8b": "hs"
        }
    ]

    this.init = function () {
        this.getFileExtension();
    };

    this.getFileExtension = function () {
        var that = this;
        this.form.keyup(function(event) {
            var text = that.form.val();

            if (text.lastIndexOf('.') != -1) {
                var extension = text.substr((text.lastIndexOf('.') + 1));
                that.GetLanguage(extension); // Using that for this scope
            }

            event.preventDefault();

        }).keyup();

    };

    this.GetLanguage = function (ext) {
            for (var i = 0; i < this.langs.length; i++){
                var obj = this.langs[i];
                for (var key in obj){
                    var attrName = key;
                    var attrValue = obj[key];
                    if(ext == attrValue){
                        var lang = attrName.substring(0, attrName.indexOf('-'));
                        var color = attrName.substring(attrName.indexOf('-') + 1);
                        console.log (lang, color);
                        this.CreateMessage(lang, color);
                        break;
                }
            }
        }
    };

    this.CreateMessage = function (language, color) {
        this.output.val(language)
            .css('color', `${color}`)
            .css('font-weight','bold');
    };
}