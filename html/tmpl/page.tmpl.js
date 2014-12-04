(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['page.tmpl'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return escapeExpression(((helper = (helper = helpers.page_title || (depth0 != null ? depth0.page_title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"page_title","hash":{},"data":data}) : helper)));
  },"3":function(depth0,helpers,partials,data) {
  return "Tripster";
  },"5":function(depth0,helpers,partials,data) {
  var stack1, buffer = "      <div class=\"col-sm-4 col-sm-offset-3\">\r\n        <div class=\"navbar-form navbar-right\">\r\n          <div class=\"input-group\">\r\n            <form id=\"search-form\" action=\"javascript:void(0);\">\r\n              <input id=\"search-query\" type=\"text\" class=\"form-control\" ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.q : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">\r\n            </form>\r\n            <span class=\"input-group-btn\">\r\n              <button id=\"search-submit\" class=\"btn btn-default\" type=\"button\">Search</button>\r\n            </span>\r\n          </div>\r\n        </div>\r\n      </div>\r\n";
},"6":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "placeholder=\""
    + escapeExpression(((helper = (helper = helpers.q || (depth0 != null ? depth0.q : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"q","hash":{},"data":data}) : helper)))
    + "\"";
},"8":function(depth0,helpers,partials,data) {
  return "col-sm-offset-7";
  },"10":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "              <a>Logged in as <b>"
    + escapeExpression(((helper = (helper = helpers.username || (depth0 != null ? depth0.username : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"username","hash":{},"data":data}) : helper)))
    + "</b></a>\r\n";
},"12":function(depth0,helpers,partials,data) {
  return "              <a href=\"./login.html\">Login</a>\r\n";
  },"14":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing;
  stack1 = ((helper = (helper = helpers.standalone || (depth0 != null ? depth0.standalone : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"standalone","hash":{},"data":data}) : helper));
  if (stack1 != null) { return stack1; }
  else { return ''; }
  },"16":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "\r\n  <div class=\"row\">\r\n    <div class=\"col-sm-";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.page_sidebar : depth0), {"name":"if","hash":{},"fn":this.program(17, data),"inverse":this.program(19, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\">\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.page_header : depth0), {"name":"if","hash":{},"fn":this.program(21, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "      <div class=\"panel panel-default\">";
  stack1 = ((helper = (helper = helpers.page_body || (depth0 != null ? depth0.page_body : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"page_body","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\r\n    </div>\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.page_sidebar : depth0), {"name":"if","hash":{},"fn":this.program(23, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </div>\r\n";
},"17":function(depth0,helpers,partials,data) {
  return "9";
  },"19":function(depth0,helpers,partials,data) {
  return "12";
  },"21":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "      <div class=\"page-header\">\r\n        <h1>"
    + escapeExpression(((helper = (helper = helpers.page_header || (depth0 != null ? depth0.page_header : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"page_header","hash":{},"data":data}) : helper)))
    + "</h1>\r\n      </div>\r\n";
},"23":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "    <div class=\"col-sm-3\">\r\n      <div class=\"panel panel-default\">";
  stack1 = ((helper = (helper = helpers.page_sidebar || (depth0 != null ? depth0.page_sidebar : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"page_sidebar","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\r\n    </div>\r\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<title>";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.page_title : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</title>\r\n<nav class=\"navbar navbar-default navbar-static-top\" role=\"navigation\">\r\n  <div class=\"container\">\r\n    <div class=\"row\">\r\n      <div class=\"col-sm-2\"><a class=\"navbar-brand\" href=\"./index.html\">Tripster</a></div>\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.username : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "      <div class=\"col-sm-3 ";
  stack1 = helpers.unless.call(depth0, (depth0 != null ? depth0.username : depth0), {"name":"unless","hash":{},"fn":this.program(8, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\">\r\n        <div class=\"navbar-right\">\r\n          <ul class=\"nav navbar-nav\">\r\n            <li>\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.username : depth0), {"name":"if","hash":{},"fn":this.program(10, data),"inverse":this.program(12, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </li>\r\n          </ul>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </div>\r\n</nav>\r\n<div class=\"container\">\r\n  ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.standalone : depth0), {"name":"if","hash":{},"fn":this.program(14, data),"inverse":this.program(16, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\r\n<footer class=\"footer\" style=\"position: absolute; bottom: 0; width: 100%; height: 60px; background-color: #f5f5f5;\">\r\n  <div class=\"container text-center\">\r\n    <p style=\"margin: 20px 0;\">Things like copyrights, attributions, licenses, etc. go here ~ (C) 2014</p>\r\n  </div>\r\n</footer>\r\n<script type=\"text/javascript\">\r\n  $('#search-form').submit(function(e) {\r\n    window.location = './search.html?q=' + encodeURIComponent($('#search-query').val());\r\n  });\r\n  $('#search-submit').click(function(e) { $('#search-form').submit(); });\r\n</script>";
},"useData":true});
})();