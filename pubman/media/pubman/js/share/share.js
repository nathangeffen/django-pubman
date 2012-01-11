/**
 * iBegin Share 2.6 (Build 1606)
 * For more info & download: http://www.ibegin.com/labs/share/
 * Created as a part of the iBegin Labs Project - http://www.ibegin.com/labs/
 * For licensing please see readme.html (MIT Open Source License)
*/

var iBeginShare = function() {
	var _pub = {
		// Change this to your base URL
		// This only affects a couple plugins, and realistically should be removed
		// from the share framework.
		base_url: './',
		
		// Default skin values
		default_skin: 'default',
		default_link: 'button',
		default_link_skin: 'default',
		
		// Set script handler to the relative path of the script which will handle
		// stats logging.
		// This is very limited at the moment, if you want to create a new backend
		// please contact us first for support, so we may improve upon this.
		script_handler: false,

		// The little thing that appears in the corner to close the box.
		close_label: 'X',

		// The label which appears for both included widgets.
		text_link_label: 'Share',
		
		// STOP EDITING
		// These are replaced by our automagic subversion handler with the current
		// tag and revision.
		version_number: '2.6',
		build_number: '1606',
		
		// Don't you love browser inconsistencies?
		is_opera: navigator.userAgent.indexOf('Opera/9') != -1,
		is_ie: navigator.userAgent.indexOf("MSIE ") != -1,
		is_safari: navigator.userAgent.indexOf('webkit') != -1,
		is_ie6: false /*@cc_on || @_jscript_version < 5.7 @*/,
		is_firefox: navigator.appName == "Netscape" && navigator.userAgent.indexOf("Gecko") != -1 && navigator.userAgent.indexOf("Netscape") == -1,
		is_mac: navigator.userAgent.indexOf('Macintosh') != -1,
		http: null,

		/**
		 * Generic function to enable the default PHP logging platform
		 * This has to be called after `base_url` is set.
		 */
		enableStats: function() {
			_pub.script_handler = _pub.base_url + 'share.php?action=log';
		},
		/**
		 * Creates an HTML element.
		 */
		createElement: function(tag, params) {
			var el = document.createElement(tag);
			if (!params) return el;
			for (var key in params) {
				if (key == 'className') el.className = params[key];
				else if (key == 'text') el.appendChild(document.createTextNode(params[key]));
				else if (key == 'html') el.innerHTML = params[key];
				else if (key == 'id') el.id = params[key];
				else if (key == 'children') continue;
				else if (key == 'events') {
					for (var name in params[key]) _pub.addEvent(el, name, params[key][name]);
				}
				else if (key == 'styles') {
					for (var name in params[key]) {
						el.style[name] = params[key][name];
					}
				}
				else el.setAttribute(key, params[key]);
			}
			if (params.children) for (var i=0; i<params.children.length; i++) el.appendChild(params.children[i]);
			return el;
		},
		/**
		 * Parses the arguments in the rel attribute
		 * @param {String} query
		 */
		parseQuery: function(query) {
			 var params = new Object();
			 if (!query) return params; 
			 var pairs = query.split(/[;&]/);
			 var end_token;
			 for (var i=0; i<pairs.length; i++) {
					var keyval = pairs[i].split('=');
					if (!keyval || keyval.length != 2) continue;
					var key = unescape(keyval[0]);
					var val = unescape(keyval[1]);
					val = val.replace(/\+/g, ' ');
					if (val[0] == '"') var token = '"';
					else if (val[0] == "'") var token = "'";
					else var token = null;
					if (token) {
						if (val[val.length-1] != token) {
							do {
								i += 1;
								val += '&'+pairs[i];
							}
							while ((end_token = pairs[i][pairs[i].length-1]) != token)
						}
						val = val.substr(1, val.length-2);
					}
					if (val == 'true') val = true;
					else if (val == 'false') val = false;
					else if (val == 'null') val = null;
					params[key] = val;
			 }
			 return params;
		},
		/**
		 * Serializes form elements into an object-array.
		 * @return {Object}
		 */
		serializeFormData: function(form) {
				var data = {};
				var els = form.getElementsByTagName('input');
				for (var i=0, el=null; (el=els[i]); i++) {
						if (el.name) {
								if (el.type == 'text' || el.type == 'hidden' || el.type == 'password'
										|| ((el.type == 'radio' || el.type == 'checkbox') && el.checked))
										data[el.name] = encodeURIComponent(el.value);
						}
				}
				var els = form.getElementsByTagName('textarea');
				for (var i=0, el=null; (el=els[i]); i++) {
						if (el.name) data[el.name] = encodeURIComponent(el.value);
				}
				var els = form.getElementsByTagName('select');
				for (var i=0, el=null; (el=els[i]); i++) {
						if (el.name) data[el.name] = encodeURIComponent(el[el.selectedIndex].value);
				}
				return data;
		},
		/**
		 * Returns a string that is considered safe for keys and slugs.
		 * @param {String} string
		 * @return {String} string
		 */
		makeSafeString: function(string) {
			return string.replace(/[^a-zA-Z0-9_-s.]/, '').toLowerCase()
		},
		/**
		 * Outputs a GET parameter string from an object array.
		 * @param {Object} params
		 * @return {String}
		 */
		createParametersString: function(params) {
			var parameters = ''; // string version of params
			for (var key in params) {
					if (typeof params[key] == 'object')
							for (var i=0; i<params[key].length; i++)
									parameters += (key + '=' + encodeURIComponent(params[key][i]) + '&');
					else
							parameters += (key + '=' + encodeURIComponent(params[key]) + '&');
			}
			return parameters;
		},
		/**
		 * Initiates an XMLHttpRequest and executes callback(responseText)
		 * @param {String} url Request url
		 * @param {Object} params Request parameters in an object-array format
		 * @param {Function} success Successful callback function
		 * @param {Function} error Error callback function
		 */
		ajaxRequest: function(url, method, params, success, error) {
			if (!method) var method = 'GET';
			var parameters = _pub.createParametersString(params);
			if (method == 'GET' && parameters) {
				if (url.indexOf('?')) url += '&' + parameters;
				else url += '?' + parameters;
			}
			_pub.http.open(method, url, true);
			_pub.http.onreadystatechange = function() {
					if (_pub.http.readyState == 4) {
							if (_pub.http.status == 200)
									success(_pub.http.responseText);
							else
									if (error)
											error(_pub.http, _pub.http.responseText);
					}
			}
			_pub.http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			if (method == 'POST') _pub.http.setRequestHeader("Content-length", parameters.length);
			_pub.http.setRequestHeader("Connection", "close");
			_pub.http.send(parameters);
		},
		showLoadingBar: function() {
			containers.loading.style.display = 'block';
			containers.content_inner.style.display = 'none';
		},
		hideLoadingBar: function() {
			containers.loading.style.display = 'none';
			containers.content_inner.style.display = 'block';
		},
		hasClass: function(obj, className) {
				if (obj.className) {
						var arrList = obj.className.split(' ');
						var strClassUpper = className.toUpperCase();

						for (var i=0; i<arrList.length; i++) {
								if (arrList[i].toUpperCase() == strClassUpper) {
										return true;
								}
						}
				}
				return false;
		},
		toggleClass: function(obj, className) {
			if (_pub.hasClass(obj, className)) _pub.removeClass(obj, className);
			else _pub.addClass(obj, className);
		},
		addClass: function(obj, className) {
			obj.className = (obj.className ? obj.className + ' ' + className : className);
		},
		removeClass: function(obj, className) {
			if (obj.className) {
				var arrList = obj.className.split(' ');
				var strClassUpper = className.toUpperCase();

				for (var i=0; i<arrList.length; i++) {
					if (arrList[i].toUpperCase() == strClassUpper) {
						arrList.splice(i, 1);
						i--;
					}
				}
				obj.className = arrList.join(' ');
			}
		},
		/**
		 * Empties the content of an object.
		 */
		empty: function(obj) {
			while (obj.firstChild) obj.removeChild(obj.firstChild);
		},
		/**
		 * Updates the content of the share box
		 * @param {HTMLObject|String} html
		 */
		html: function(html) {
			if (!html) return;
			_pub.hideLoadingBar();
			_pub.empty(containers.content_inner);
			if (typeof(html) == 'string') containers.content_inner.innerHTML = html;
			else containers.content_inner.appendChild(html);
		},
		/**
		 * Hides the share box.
		 */
		hide: function() {
			if (active.tab && active.tab.plugin.unload) active.tab.plugin.unload();
			if (active.link) _pub.removeClass(active.link, 'share-active');
			active = {}
			containers.box.style.display = 'none';
			_pub.addClass(containers.box, 'share-box-show');
		},
		/**
		 * Shows the share box and (if obj is present) positions
		 * it relative to the container.
		 * @param {HTMLObject} obj
		 * @param {Object} params
		 */
		show: function(obj, params) {
			// if no plugins are active bail
			if (!_pub.plugins.list.length) return false;
			// if the current link is active bail
			if (active.link == obj) return false;

			if (!params) var params = {};
			
			if (!params.link) params.link = window.location.href;
			if (!params.title) params.title = document.title;
			if (!params.skin) params.skin = _pub.default_skin;
			
			// hide it first to stop the bug where active button still shows
			if (active.link) _pub.hide();

			active.link = obj;
			active.link.params = params;

			_pub.addClass(obj, 'share-active');
			
			if (!params.skin) params.skin = 'default';
						
			containers.box.className = 'share-skin-' + params.skin;
			
			containers.box.style.position = 'absolute';
			containers.box.style.display = 'block';
			containers.box.style.visibility = 'hidden';
			containers.box.style.top = 0;
			containers.box.style.left = 0;

			var curtop = curleft = 0;
			var border;
			curtop += obj.offsetHeight + 5;
			if (obj.getBoundingClientRect) {
				var bounds = obj.getBoundingClientRect();
				curleft += bounds.left - 2;
				curtop += bounds.top + document.documentElement.scrollTop - 2;
			}
			else if (obj.offsetParent) {
				do {
					// XXX: If the element is position: relative we have to add borderWidth
					if (_pub.getStyle(obj, 'position') == 'relative') {
						if (border = _pub.getStyle(obj, 'border-top-width')) curtop += parseInt(border);
						if (border = _pub.getStyle(obj, 'border-left-width')) curleft += parseInt(border);
					}
					else if (obj.currentStyle && obj.currentStyle.hasLayout && obj !== document.body) {
						curleft += obj.clientLeft;
						curtop += obj.clientTop;
					}

					curtop += obj.offsetTop;
					curleft += obj.offsetLeft;
				}
				while (obj = obj.offsetParent)
			}
			else if (obj.x) {
				curtop += obj.y;
				curleft += obj.x;
			}
			
			pagesize = _pub.getPageSize();
			if (containers.box.offsetWidth + curleft > pagesize.width) {
				// if the box is larger than the page width, set it to 20px on the left
				if (containers.box.offsetWidth > pagesize.width-20) {
				 curleft = 20;
				}
				else {
					// otherwise set it to page width - box length - 20px
					curleft = pagesize.width-20-containers.box.offsetWidth;
				}
			}
			containers.box.style.top = curtop + 'px';
			containers.box.style.left = curleft + 'px';
			containers.box.style.visibility = 'visible';
			_pub.removeClass(containers.box, 'share-box-show');

			for (var i=0; i<_pub.plugins.list.length; i++) {
				var cur = _pub.plugins.list[i];
				var valid = true;
				if (cur.requires) {
					// validate variables exist in the params for the plugin
					for (var z=0; z<cur.requires.length; z++) {
						if (!params || !params[cur.requires[z]]) {
							valid = false;
							break;
						}
					}
				}
				if (valid) cur.tab.style.display = 'block';
				else cur.tab.style.display = 'none';
				cur.tab.className = '';
			}
			active.tab = _pub.plugins.list[0].tab;
			active.tab.className = 'active';
			active.tab.plugin.render(_pub.showPlugin, params);
		},
		
		/**
		 * Gets the page constraints
		 */
		getPageSize: function() {
			return {
				width: window.innerWidth || (document.documentElement && document.documentElement.clientWidth) || document.body.clientWidth,
				height: window.innerHeight || (document.documentElement && document.documentElement.clientHeight) || document.body.clientHeight
			};
		},
		
		showPlugin: function(html, params) {
			_pub.html(html);
			var h2 = _pub.createElement('h2', {html: active.tab.plugin.label});
			containers.content_inner.insertBefore(h2, containers.content_inner.firstChild);
		},
		handleLink: function(e) {
			if (!e) var e = window.event;
			var obj = e.target ? e.target : e.srcElement;
			if (e.preventDefault) e.preventDefault();
			var params = (obj.params ? obj.params : _pub.parseQuery(obj.getAttribute('rel')));
			if (_pub.hasClass(obj, 'share-active')) iBeginShare.hide(obj);
			else iBeginShare.show(obj, params);
		},
		/**
		 * Draws a link on an object immediately.
		 * @param {HTMLObject} obj
		 * @param {Object} params
		 * @param {String} skin
		 */
		drawLink: function(obj, params) {
			if (params === undefined) var params = {}
			if (params.link_style === undefined) params.link_style = _pub.default_link;
			if (params.link_skin === undefined) params.link_skin = _pub.default_link_skin;
			if (params.link_label === undefined) params.link_label = _pub.text_link_label;
						
			var link = _pub.createElement('a', {
				className: 'share-link',
				href: 'javascript:void(0)',
				html: params.link_label,
				events: {
					click: _pub.handleLink
				}
			});
			link.params = params;

			obj.appendChild(_pub.createElement('span', {
				className: 'share-link-wrapper share-link-' + params.link_style + ' share-link-' + params.link_style + '-' + params.link_skin,
				children: [link]
			}));
		},
		/**
		 * Draws a button on an object immediately.
		 * @param {HTMLObject} obj
		 * @param {Object} params
		 */
		drawButton: function(obj, params) {
			params.link_style = 'button';
			_pub.drawLink(obj, params);
		},
		/**
		 * Draws a text link on an object immediately.
		 * @param {HTMLObject} obj
		 * @param {Object} params
		 */
		drawTextLink: function(obj, params) {
			params.link_style = 'text';
			_pub.drawLink(obj, params);
		},
		/**
		 * Attaches a share link to an object when the page is loaded.
		 * @param {HTMLObject|String} obj
		 * @param {Object} params
		 * @param {String} skin
		 */
		attachLink: function(obj, params) {
			if (typeof(obj) == 'string') obj = document.getElementById(obj);
			_pub.addEvent(window, 'load', _pub.bind(function(e, obj, params){iBeginShare.drawLink(obj, params);}, obj, params));
		},
		/**
		 * Attaches a button to an object when the page is loaded.
		 * @param {HTMLObject|String} obj
		 * @param {Object} params
		 */
		attachButton: function(obj, params) {
			params.link_style = 'button';
			_pub.attachLink(obj, params);
		},
		/**
		 * Attaches a text link to an object when the page is loaded.
		 * @param {HTMLObject|String} obj
		 * @param {Object} params
		 */
		attachTextLink: function(obj, params) {
			params.link_style = 'text';
			_pub.attachLink(obj, params);
		},
		/**
		 * Binds arguments to a callback function
		 */
		bind: function(fn) {
				var args = [];
				for (var n=1; n<arguments.length; n++) args.push(arguments[n]);
				return function(e) { return fn.apply(this, [e].concat(args)); };
		},
		/**
		 * Binds an event listener
		 * @param {Object} obj Object to bind the event to.
		 * @param {String} evType Event name.
		 * @param {Function} fn Function callback reference.
		 */
		addEvent: function(obj, evType, fn) {
			if (obj.addEventListener) {
				obj.addEventListener(evType, fn, false);
				return true;
			}
			else if (obj.attachEvent) {
				var r = obj.attachEvent("on"+evType, fn);
				return r;
			}
			else {
				return false;
			}
		},
		getStyle: function(obj, styleProp) {
			if (obj.currentStyle)
				return obj.currentStyle[styleProp];
			else if (window.getComputedStyle)
				return document.defaultView.getComputedStyle(obj,null).getPropertyValue(styleProp);
		},
		getContainer: function() {
			return containers.box;
		},
		/**
		 * If `script_handler` is enabled this will return a URL which will log the action.
		 * @param {String} url
		 * @param {String} label The label for the log action (e.g. 'Delicious').
		 */
		makeLoggableUrl: function(link, to, name) {
			if (!_pub.script_handler) return to;
			if (name === undefined) var name = '';
			var log_key = active.tab.plugin.log_key;
			if (!log_key) var log_key = _pub.makeSafeString(active.tab.plugin.label);
			return _pub.script_handler + '&plugin=' + encodeURIComponent(log_key) + '&name=' + encodeURIComponent(name) + '&link=' + encodeURIComponent(link) + '&to=' + encodeURIComponent(to) + '&' + ts();
		},
		plugins: {
			builtin: {
				bookmarks: function() {
					var bookmarks_per_line = 7;
					var lines_per_page = 2;

					var current_page;
					var link;
					var title;

					var getIcon = function(name) {
						return 'bm_' + _pub.makeSafeString(name);
					}

					var services = new Array();
					var selectThisPage = function(e) {
						if (!e) var e = window.event;
						var obj = e.target ? e.target : e.srcElement;
						selectPage(obj.getAttribute('rel'));
						if (e.preventDefault) e.preventDefault();
						return false;
					};
					var selectPage = function(n) {
						if (current_page == n) return;
						var el = document.getElementById('bm_page_' + current_page);
						if (el) el.className = '';
						var tbody = container.getElementsByTagName('tbody')[0];
						_pub.empty(tbody);
						var end = n*(lines_per_page*bookmarks_per_line);
						var start = end-(lines_per_page*bookmarks_per_line);
						var tr = _pub.createElement('tr');
						for (var i=start; i<end; i++) {
							if (!services[i]) break;
							if (i % bookmarks_per_line == 0 && i != 0) {
								tbody.appendChild(tr);
								tr = _pub.createElement('tr');
							}
							tr.appendChild(_pub.createElement('td', {
								styles: {
									textAlign: 'center',
									width: 100/bookmarks_per_line + '%'
								},
								children: [
									_pub.createElement('a', {
										title: services[i][0],
										target: '_blank',
										href: _pub.makeLoggableUrl(link, services[i][1].replace('__URL__', link).replace('__TITLE__', title), services[i][0]),
										html: services[i][0],
										styles: {
											textDecoration: 'none'
										},
										children: [
											_pub.createElement('img', {
												src: _pub.base_url + 'images/icons/' + getIcon(services[i][0]) + '.gif',
												alt: ''
											})
										]
									})
								]
							}));
						}
						tbody.appendChild(tr);
						current_page = n;
						var el = document.getElementById('bm_page_' + current_page);
						if (el) el.className = 'active';
					}
					var container = null;

					return {
						log_key: 'bookmarks',
						label: 'Bookmarks',
						requires: ['link', 'title'],
						addService: function(name, url) {
							services.push([name, url]);
						},
						render: function(callback, params) {
							current_page = null;
							link = encodeURIComponent(params.link);
							title = encodeURIComponent(params.title);

							var total_pages = Math.ceil(services.length/(lines_per_page*bookmarks_per_line));
							
							container = _pub.createElement('table', {
								cellPadding: 0,
								cellSpacing: 0,
								styles: {
									border: 0
								},
								children: [
									_pub.createElement('tbody')
								]
							});
							
							if (total_pages > 1) {
								var pages = new Array();
								for (var i=1; i<=total_pages; i++) {
									pages.push(_pub.createElement('a', {
										id: 'bm_page_' + i,
										html: i,
										href: '#',
										title: 'Page ' + i,
										className: (i == 1 ? 'active': ''),
										rel: i,
										events: {
											click: selectThisPage
										}
									}));
								}
								container.appendChild(_pub.createElement('tfoot', {
									children: [_pub.createElement('tr', {
										children: [
											_pub.createElement('td', {
												colSpan: bookmarks_per_line,
												children: pages
											})
										]
									})]
								}));
							}
							selectPage(1);
							callback(container, params);
						}
					}
				}(),

				email: function() {
					var allow_message = true;
					var data_store = {};
					var msg_container = null;
					var form_container = null;

					var createInputCell = function(label, name, value) {
						return _pub.createElement('td', {
							children: [
								_pub.createElement('label', {
									htmlFor: 'id_share_mail_' + name,
									id: 'label_share_mail_' + name,
									html: label,
									styles: {
										display: 'block'
									}
								}),
								_pub.createElement('input', {
									type: 'text',
									name: name,
									id: 'id_share_mail_' + name,
									value: value || ''
								})
							]
						});
					}
					
					var validateFields = function() {
						var fields = ['from_name', 'from_email', 'to_name', 'to_email'];
						var valid = true;
						for (var i=0; i<fields.length; i++) {
							var el = document.getElementById('label_share_mail_' + fields[i]);
							if (!document.getElementById('id_share_mail_' + fields[i]).value) {
								el.style.color = 'red';
								valid = false;
							}
							else {
								el.style.color = '';
							}
						}
						if (!valid) {
							_pub.empty(msg_container);
							msg_container.style.color = 'red';
							msg_container.appendChild(document.createTextNode('Please fill in required fields.'));
						}
						return valid;
					}

					return {
						log_key: 'email',
						label: 'Email',
						requires: ['link', 'title'],
						unload: function() {
							var base = document.forms['share_form_email'];
							if (!base) return;
							data_store = _pub.serializeFormData(form_container);
						},
						render: function(callback, params) {
							
							msg_container = _pub.createElement('span', {
								styles: {
									paddingLeft: '10px'
								}
							});
							
							row_sets = [
								_pub.createElement('tr', {
								children: [
										createInputCell('Your name:', 'from_name', data_store.share_mail_frnme),
										createInputCell('Your email:', 'from_email', data_store.share_mail_freml)
									]
								}),
								_pub.createElement('tr', {
									children: [
										createInputCell("Friend's name:", 'to_name', data_store.share_mail_tonme),
										createInputCell("Friend's email:", 'to_email', data_store.share_mail_toeml)
									]
								})
							];
							
							if (allow_message) {
								row_sets.push(_pub.createElement('tr', {
									children: [
										_pub.createElement('td', {
											colSpan: 2,
											children: [
												_pub.createElement('label', {
													htmlFor: 'id_share_mail_message',
													html: 'Message: ',
													children: [
														_pub.createElement('span', {
															html: '(Optional)'
														})
													],
													styles: {
														display: 'block'
													}
												}),
												_pub.createElement('textarea', {
													name: 'message',
													id: 'id_share_mail_message',
													value: data_store.share_mail_msg || ''
												})
											]
										})
									]
								}));
							}
							row_sets.push(_pub.createElement('tr', {
								children: [
									_pub.createElement('td', {
										colSpan: 2,
										children: [
											_pub.createElement('input', {
												type: 'submit',
												value: 'Send',
												className: 'button'
											}),
											msg_container
										]
									})
								]
							}));
							
							form_container = _pub.createElement('form', {
								method: 'get',
								name: 'share_form_email',
								events: {
									submit: function(e) {
										if (!e) var e = window.event;
										var obj = e.target ? e.target : e.srcElement;
										if (e.preventDefault) e.preventDefault();
										if (!validateFields()) return false;
										_pub.empty(msg_container);
										msg_container.appendChild(document.createTextNode('Sending Request...'));
										data = _pub.serializeFormData(obj);
										data.link = params.link;
										data.action = 'email';
										data.title = params.title;
										var url = _pub.makeLoggableUrl(params.link, _pub.base_url + 'plugins/email/email.php?' + _pub.createParametersString(data) + '&' + ts());
										_pub.ajaxRequest(url, 'GET', {}, function(response) {
											callback('<div style="padding: 20px 0; font-size: 1.2em; font-weight: bold; color: green;">' + response + '</div>', params);
										}, function(http, response) {
											msg_container.style.color = 'red';
											// 400 means invalid data
											_pub.empty(msg_container);
											if (http.status == 400)
												msg_container.appendChild(document.createTextNode(response));
											else
												msg_container.appendChild(document.createTextNode('Error processing your request.'));
										});
										return false;
									}
								},
								children: [
									table = _pub.createElement('table', {
										cellPadding: 0,
										cellSpacing: 0,
										styles: {
											border: 0
										},
										children: [
											_pub.createElement('tbody', {
												children: row_sets
											})
										]
									})
								]
							});
							callback(form_container, params);
						}
					}
				}(),

				mypc: function() {
					function createDocumentRow(type, label, params) {
						var link = encodeURIComponent(params.link);
						var title = encodeURIComponent(params.title);
						var content = encodeURIComponent(params.content);
						
						return _pub.createElement('tr', {
							children: [
								_pub.createElement('td', {
									styles: {
										width: '10%',
										paddingLeft: '50px'
									},
									children: [
										_pub.createElement('a', {
											href: _pub.makeLoggableUrl(params.link, _pub.base_url + 'plugins/mypc/mypc.php?action='+type+'&link='+link+'&content='+content+'&title='+title+'&'+ts(), type),
											title: label,
											children: [
												_pub.createElement('img', {
													src: _pub.base_url + 'images/icons/pc_'+type+'.gif',
													styles: {
														width: '40px',
														height: '40px'
													}
												})
											]
										})
									]
								}),
								_pub.createElement('td', {
									children: [
										_pub.createElement('a', {
											href: _pub.makeLoggableUrl(params.link, _pub.base_url + 'plugins/mypc/mypc.php?action='+type+'&link='+link+'&content='+content+'&title='+title+'&'+ts()),
											html: label
										})
									]
								})
							]
						});
					}
					return {
						log_key: 'mypc',
						label: 'My Computer',
						requires: ['link', 'title', 'content'],
						render: function(callback, params) {
							var container = _pub.createElement('div', {
								children: [
									_pub.createElement('table', {
										cellPadding: 0,
										cellSpacing: 0,
										styles: {
											border: 0
										},
										children: [
											_pub.createElement('tbody', {
												children: [
													createDocumentRow('pdf', 'PDF - Portable Document Format', params),
													createDocumentRow('word', 'Microsoft Word, Wordpad, Works', params)
												]
											})
										]
									})
								]
							})

							callback(container, params);
						}
					}
				}(),

				printer: function() {
					return {
						log_key: 'printer',
						label: 'Printer',
						requires: ['content'],
						render: function(callback, params) {
							var link = encodeURIComponent(params.link);
							var title = encodeURIComponent(params.title);
							var content = encodeURIComponent(params.content);
							var url = _pub.makeLoggableUrl(params.link, _pub.base_url+'plugins/print/print.php?link='+link+'&title='+title+'&content='+content+'&'+ts());

							var table = _pub.createElement('table', {
								cellPadding: 0,
								cellSpacing: 0,
								styles: {
									border: 0
								},
								children: [
									_pub.createElement('tbody', {
										children: [
											_pub.createElement('tr', {
												children: [
													_pub.createElement('td', {
														styles: {
															textAlign: 'center'
														},
														children: [
															_pub.createElement('a', {
																href: 'javascript:void(0)',
																title: 'Print this Document',
																events: {
																	click: function() {
																		window.open(url, '', 'scrollbars=yes,menubar=no,height=600,width=800,resizable=yes,toolbar=no,location=no,status=no'); 
																		return false;
																	}
																},
																children: [
																	_pub.createElement('img', {
																		src: _pub.base_url + 'images/icons/print.gif',
																		styles: {
																			width: '40px',
																			height: '40px'
																		}
																	}),
																	_pub.createElement('div', {
																		html: 'Print'
																	})
																]
															})
														]
													})
												]
											})
										]
									})
								]
							});
							callback(table, params);
						}
					}
				}()
			},
			list: new Array(),
			/**
			 * Registers a plugin.
			 * @param {Function} func
			 * @param {Function} func
			 * @param {Function} ...
			 */
			register: function() {
				for (var i=0; i<arguments.length; i++) {
					_pub.plugins.list.push(arguments[i]);
					loadPlugin(arguments[i]);					
				}
				return true;
			},
			/**
			 * Unregisters a plugin.
			 * @param {Function} func
			 * @param {Function} func
			 * @param {Function} ...
			 */
			unregister: function() {
				var new_list = new Array();
				var to_unregister = new Array();
				for (var i=0; i<arguments.length; i++) {
					to_unregister.push(arguments[i]);
				}
				for (var i=0; i<_pub.plugins.list.length; i++) {
					var exists = false;
					for (var z=0; z<to_unregister.length; z++) {
						if (_pub.plugins.list[i] == to_unregister[z]) exists = true;
					}
					if (!exists) new_list.push(_pub.plugins.list[i]);
				}
				if (_pub.plugins.list.length == new_list.length) return false;
				_pub.plugins.list = new_list;
				return true;
			}
		}
	};
	var containers = {};
	var active = {};
	/**
	 * Creates a new XMLHttpRequest object based on browser.
	 */
	var createXMLHttpRequest = function() {
		var http;
		if (window.XMLHttpRequest) { // Mozilla, Safari,...
			http = new XMLHttpRequest();
			if (http.overrideMimeType) {
				// set type accordingly to anticipated content type
				http.overrideMimeType('text/html');
			}
		}
		else if (window.ActiveXObject) { // IE
			try {
				http = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					http = new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {}
			}
		}
		if (!http) {
			alert('Cannot create XMLHTTP instance');
			return false;
		}
		return http;
	};
	/**
	 * Returns a random number
	 */
	var ts = function() { return Math.floor(Math.random()*10000001); };
	/**
	 * Creates the iBegin Share base object.
	 */
	var create = function() {
		containers.box = _pub.createElement('div', {
			id: 'share-box',
			styles: {
				display: 'none'
			},
			children: [
				_pub.createElement('a', {
					title: 'Close',
					id: 'share-close',
					href: 'javascript:void(0)',
					html: _pub.close_label,
					events: {
						click: function(e) { iBeginShare.hide(); return false; }
					}
				})
			]
		});

		containers.inner = _pub.createElement('div', {
			id: 'share-box-inner'
		});
		
		containers.menu = _pub.createElement('ul', {
			id: 'share-menu'
		});
		containers.inner.appendChild(containers.menu);
		
		for (var i=0; i<_pub.plugins.list.length; i++) loadPlugin(_pub.plugins.list[i]);
		
		containers.content = _pub.createElement('div', {
			id: 'share-content'
		});
		containers.content.appendChild(document.createElement('br'));
		
		// TODO: update css with loading image
		containers.loading = _pub.createElement('div', {
			id: 'share-loading',
			styles: {
				display: 'none'
			}
		});
		containers.content.appendChild(containers.loading);
		
		containers.content_inner = _pub.createElement('div', {
			id: 'share-content-inner'
		});
		containers.content.appendChild(containers.content_inner);
		containers.inner.appendChild(containers.content);

		containers.box.appendChild(containers.inner);
		document.body.appendChild(containers.box);

		return containers.box;
	};
	/**
	 * Registers a plugin with the share object.
	 * @param {Object} plugin
	 */
	var loadPlugin = function(plugin) {
		// if we're not initialized yet don't create it
		if (!containers.box) return;
		// <li class="class_name"><a href="#"><span>Label</span></a></li>
		var tab = _pub.createElement('li', {
			children: [
				_pub.createElement('a', {
					href: 'javascript:void(0)',
					children: [
						_pub.createElement('span', {
							html: plugin.label
						})
					]
				})
			]
		});
		tab.plugin = plugin;
		plugin.tab = tab;
		tab.onclick = function(e) {
			// if the current tab is active bail
			if (active.tab == tab) return false;
			_pub.showLoadingBar();
			if (active.tab.plugin.unload) active.tab.plugin.unload();
			active.tab.className = '';
			active.tab = tab;
			active.tab.className = 'active';
			plugin.render(_pub.showPlugin, active.link.params);
			return false;
		}
		containers.menu.appendChild(tab);
		return tab;
	};
	/**
	 * Initializes the iBegin Share namespace.
	 */
	var initialize = function() {
		create();
		document.body.style.position = 'relative';
		var els = document.getElementsByTagName('script');
		var src;
		for (var i=0, el=null; (el = els[i]); i++) {
			if (!(src = el.getAttribute('src'))) continue;
			src = src.split('?')[0];
			if (src.substr(src.length-9) == '/share.js') {
				_pub.base_url = src.substr(0, src.length-8);
				break;
			}
		}
		_pub.http = createXMLHttpRequest();
	};
	
	_pub.addEvent(window, 'load', initialize);
	_pub.addEvent(window, 'keypress', function(e){ if (e.keyCode == (window.event ? 27 : e.DOM_VK_ESCAPE)) { iBeginShare.hide(); }});
	
	return _pub;
}();
// See readme/index.html for information on adding bookmarks
iBeginShare.plugins.builtin.bookmarks.addService('Facebook', 'http://www.facebook.com/share.php?src=bm&u=__URL__&t=__TITLE__&v=3');
iBeginShare.plugins.builtin.bookmarks.addService('Digg', 'http://digg.com/submit/?url=__URL__&title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('Delicious', 'http://del.icio.us/post?&url=__URL__&title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('Google', 'http://www.google.com/bookmarks/mark?op=add&title=__TITLE__&bkmk=__URL__');
iBeginShare.plugins.builtin.bookmarks.addService('Yahoo!', 'http://e.my.yahoo.com/config/edit_bookmark?.src=bookmarks&.folder=1&.name=__TITLE__&.url=__URL__&.save=+Save+');
iBeginShare.plugins.builtin.bookmarks.addService('StumbleUpon', 'http://www.stumbleupon.com/submit?url=__URL__&title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('MySpace', 'http://www.myspace.com/Modules/PostTo/Pages/?t=__TITLE__&c=%20&u=__URL__&l=2');

iBeginShare.plugins.builtin.bookmarks.addService('Technorati', 'http://technorati.com/faves?add=__URL__');
iBeginShare.plugins.builtin.bookmarks.addService('Reddit', 'http://reddit.com/submit?url=__URL__&title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('Ask', 'http://myjeeves.ask.com/mysearch/BookmarkIt?v=1.2&t=webpages&title=__TITLE__&url=__URL__');
iBeginShare.plugins.builtin.bookmarks.addService('Live', 'http://favorites.live.com/quickadd.aspx?url=__URL__&title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('Mixx', 'http://www.mixx.com/submit?page_url=__URL__');
iBeginShare.plugins.builtin.bookmarks.addService('Blinklist', 'http://www.blinklist.com/index.php?Action=Blink/addblink.php&Url=__URL__&Title=__TITLE__');
iBeginShare.plugins.builtin.bookmarks.addService('Twitter', 'http://twitter.com/home/?status=__TITLE__%3A%20__URL__');

// Uncomment any of these lines to disable plugin registration.
// Adjust the order to adjust the order of tabs.
iBeginShare.plugins.register(
	iBeginShare.plugins.builtin.bookmarks
//	iBeginShare.plugins.builtin.email
//	iBeginShare.plugins.builtin.mypc,
//	iBeginShare.plugins.builtin.printer
);