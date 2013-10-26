// ==UserScript==
// @name           CPANAutoPager
// @namespace      http://spiritloose.net/
// @author         Jiro Nishiguchi <jiro@cpan.org>
// @include        http://search.cpan.org/search*
// @description    Add autoloading for next page to CPAN search result. DblClick to enable/disable it. Original code by ma.la. see http://la.ma.la/blog/diary_200506231749.htm
// ==/UserScript==

(function(){
	var base = 'http://search.cpan.org/search';
	var offset;
	var num = 10;
	var query;
	var insertPoint;
	var Enable = -1;
	
	var watch_scroll = function(){
		try {
			var sc = document.body.scrollTop;
			var total = (document.body.scrollHeight - document.body.clientHeight);
			var remain = total - sc;
			if (remain < 500 && Enable == 1) {
				do_request()
			}
		} catch(e) {
		}
		var self = arguments.callee;
		setTimeout(self, 100);
	};
	
	var do_insert = function(v) {
		var end_flag = 0;
		var start = v.indexOf("<!--results-->");
		var end = v.indexOf('<div class="footer">');
		if (v.indexOf("Next &gt;&gt;") == -1) {
			end_flag = 1;
		}
		v = v.slice(start, end);
		var div = document.createElement("div");
		div.innerHTML = ["<hr>", offset, " to ", (offset + num), v].join("");
		document.body.insertBefore(div,insertPoint);
		window.status = "loading ... " + offset +" - " + (offset+num) + " done.";
		if (!end_flag) {
			offset += num;
		}
	};
	
	var do_request = function(){
		if(this.requested == offset){return}
		this.requested = offset;
		var xmlhttp;
		try {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
			xmlhttp.onreadystatechange = function(){
				if (xmlhttp.readyState == 4) {
					do_insert(xmlhttp.responseText);
				}
			};
			xmlhttp.open("GET", base+query.replace(/s=\d*/,"s="+offset), true);
			window.status = "loading ... " + offset +" - " + (offset+num);
			xmlhttp.send(null);
		} catch(e) {
			GM_xmlhttpRequest({
				method: "GET",
				url: base + query.replace(/s=\d*/, "s=" + offset),
				onload: function(details)
				{
					do_insert(details.responseText);
				}
			});
		}
	};
	
	var next;
	var init_autopager = function(){
		var div = document.getElementsByTagName("div");
		var len = div.length;
		for (var i = 0; i < len; i++) {
			if(div[i].className == "footer"){
				insertPoint = div[i];
			}
		}

		// find Next >>
		var a = document.getElementsByTagName("a");
		var len = a.length;
		for (var i = len - 1; i >= 0; i--) {
			var content = a[i].textContent != undefined ? a[i].textContent : a[i].innerText;
			if (content.indexOf("Next >>") != -1) {
				next = a[i];
			}
		}
		if (!next) { return }
		var href = next.href;
		query = href.substr(href.indexOf("?"));
		offset = (query.match(/s=(\d*)/))[1] - 0;
	};
	// init 
	if (window.location.href.indexOf(base) != -1) {
		if (document.body.attachEvent) {
			document.body.attachEvent(
				'ondblclick',function(){
					Enable *= -1;
					window.status = (Enable == 1) ? "Enabled" : "Disabled"
				}
			);
		} else {
			document.body.addEventListener(
				'dblclick',function(){
					Enable *= -1;
					window.status = (Enable == 1) ? "Enabled" : "Disabled"
				},true
			);
		}
		init_autopager();
		if (next) { watch_scroll() }
	}
})();
