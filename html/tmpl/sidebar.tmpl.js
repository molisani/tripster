(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['sidebar.tmpl'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, buffer = "    <div class=\"panel-body\">\r\n        <div class=\"container-fluid\">\r\n            <div class=\"row\">\r\n                <button type=\"button\" class=\"btn btn-danger pull-right\" id=\"logout-btn\">Logout</button>\r\n            </div>\r\n        </div>\r\n    </div>\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.friends : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    <script type=\"text/javascript\">\r\n    $('#logout-btn').click(function(){\r\n        $.ajax({\r\n            url: '../api/user.py', \r\n            type: 'post',\r\n            data: {\r\n                action: 'logout',\r\n                user_id: $.cookie('user_id'),\r\n                token: $.cookie('token')\r\n            },\r\n            dataType: 'json',\r\n            success: function(json) {\r\n                $.cookie('username', '', {expires: -1});\r\n                $.cookie('user_id', '', {expires: -1});\r\n                $.cookie('token', '', {expires: -1});\r\n                location.reload();\r\n            }\r\n        });\r\n    });\r\n    </script>\r\n";
},"2":function(depth0,helpers,partials,data) {
  var stack1, buffer = "        <div class=\"panel-body\">\r\n            <hr>\r\n            <span class=\"label label-primary pull-right\">Friends</span>\r\n        </div>\r\n        <table class=\"table\">\r\n            <thead></thead>\r\n            <tbody>\r\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.friends : depth0), {"name":"each","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </tbody>\r\n        </table>\r\n";
},"3":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "                    <tr><td><a href=\"./user.html?id="
    + escapeExpression(((helper = (helper = helpers.user_id || (depth0 != null ? depth0.user_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"user_id","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.fullname || (depth0 != null ? depth0.fullname : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"fullname","hash":{},"data":data}) : helper)))
    + "</a></td></tr>\r\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.username : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { return stack1; }
  else { return ''; }
  },"useData":true});
})();