// ==UserScript==
// @name           NicoVideo Add My List
// @namespace      http://spiritloose.net/
// @include        http://www.nicovideo.jp/*
// @include        http://tw.nicovideo.jp/*
// ==/UserScript==

(function(){
    // edit me!
    var GROUP_ID = 2456318;

    var w = unsafeWindow || window;
    var needWatchScroll = false;
    var addButton = function(elem, url) {
        needWatchScroll = true;
        var button = document.createElement('input');
        button.type = 'button';
        button.className = 'submit';
        button.value = '\u30DE\u30A4\u30EA\u30B9\u30C8\u306B\u8FFD\u52A0';
        var data = 'mylist=add&mylist_add=%E7%99%BB%E9%8C%B2&ajax=1&group_id=' + GROUP_ID;
        button.addEventListener('click', function(e) {
            GM_xmlhttpRequest({
                url: url,
                method: 'post',
                data: data,
                headers: { 'Content-type': 'application/x-www-form-urlencoded' },
                onload: function(req) {
                    try {
                        eval('var result = ' + req.responseText);
                        if (result.result == 'success') {
                            button.value = '\u8FFD\u52A0\u3057\u307E\u3057\u305F';
                        } else if (result.result == 'duperror') {
                            button.value = '\u3059\u3067\u306B\u8FFD\u52A0\u6E08';
                        }
                    } catch (e) {
                        button.value = 'ERROR!';
                    }
                    button.disabled = 'true';
                }
            });
        }, false);
        elem.appendChild(button);
    };
    
    var processNodes = function(nodes) {
        for (var i = 0; i < nodes.length; i++) {
            node = nodes[i];
            node.getElementsByClassName = w.document.getElementsByClassName;
            // top, tag, search, newarrival
            node.getElementsByClassName('thumb_L').each(function(elem) {
                if (elem.getElementsByTagName('input').length) return;
                var url = elem.getElementsByTagName('a')[0].href;
                addButton(elem, url);
            });

            // ranking
            node.getElementsByClassName('rank_num').each(function(elem) {
                if (elem.getElementsByTagName('input').length) return;
                var url = elem.nextSibling.nextSibling.getElementsByTagName('a')[0].href;
                if (url.indexOf('watch/') >= 0) {
                    addButton(elem, url);
                }
            });

            // random
            node.getElementsByClassName('thumb_frm').each(function(elem) {
                if (elem.getElementsByTagName('input').length) return;
                var url = elem.getElementsByTagName('a')[0].href;
                addButton(elem, url);
            });
        }
    };

    var execute = function() {
        processNodes(w.document.getElementsByTagName('body'));
    };

    // top
    if (w.switchCategoryTag) {
        var orig = w.switchCategoryTag;
        w.switchCategoryTag = function() {
            orig.apply(w, arguments);
            setTimeout(execute, 500);
        };
    }

    // AutoPagerize
    if (window.AutoPagerize != undefined) {
        window.AutoPagerize.addFilter(processNodes);
    }

    execute();

})();
