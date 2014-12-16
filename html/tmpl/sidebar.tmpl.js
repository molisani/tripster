(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['sidebar.tmpl'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"panel-body\">\r\n  <div class=\"container-fluid\">\r\n    <div class=\"row\">\r\n      <button type=\"button\" class=\"btn btn-danger pull-right\" id=\"logout-btn\">Logout</button>\r\n    </div>\r\n  </div>\r\n</div>\r\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.friends : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.rec_friend : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.trips : depth0), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.rec_locations : depth0), {"name":"if","hash":{},"fn":this.program(11, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "<script type=\"text/javascript\">\r\n$('#logout-btn').click(function(){\r\n  $.ajax({\r\n    url: '../api/user.py', \r\n    type: 'post',\r\n    data: {\r\n      action: 'logout',\r\n      user_id: $.cookie('user_id'),\r\n      token: $.cookie('token'),\r\n      id: $.cookie('user_id')\r\n    },\r\n    dataType: 'json',\r\n    success: function(json) {\r\n      $.cookie('username', '', {expires: -1});\r\n      $.cookie('user_id', '', {expires: -1});\r\n      $.cookie('token', '', {expires: -1});\r\n      location.reload();\r\n    }\r\n  });\r\n});\r\n</script>\r\n";
},"2":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"panel-body\" style=\"padding-top: 0px;\">\r\n  <hr style=\"margin-top: 5px;\"></hr>\r\n  <span class=\"label label-primary\">Friends</span>\r\n</div>\r\n<table class=\"table\">\r\n  <thead></thead>\r\n  <tbody>\r\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.friends : depth0), {"name":"each","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </tbody>\r\n</table>\r\n";
},"3":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "    <tr><td><a href=\"./user.html?id="
    + escapeExpression(((helper = (helper = helpers.user_id || (depth0 != null ? depth0.user_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"user_id","hash":{},"data":data}) : helper)))
    + "\" class=\"primary\">"
    + escapeExpression(((helper = (helper = helpers.fullname || (depth0 != null ? depth0.fullname : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"fullname","hash":{},"data":data}) : helper)))
    + "</a></td></tr>\r\n";
},"5":function(depth0,helpers,partials,data) {
  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
  return "<div class=\"panel-body\">\r\n  <span class=\"label label-primary\">Do you know?</span>\r\n</div>\r\n<table class=\"table\">\r\n  <thead></thead>\r\n  <tbody>\r\n    <tr><td><a href=\"./user.html?id="
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.rec_friend : depth0)) != null ? stack1.rec_id : stack1), depth0))
    + "\" class=\"primary\">"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.rec_friend : depth0)) != null ? stack1.rec_name : stack1), depth0))
    + "</a></td></tr>\r\n  </tbody>\r\n</table>\r\n";
},"7":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"panel-body\" style=\"padding-top: 0px;\">\r\n  <br style=\"margin-top: 5px;\"></br>\r\n  <span class=\"label label-success\">Trips</span>\r\n</div>\r\n<table class=\"table\">\r\n  <thead></thead>\r\n  <tbody>\r\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.trips : depth0), {"name":"each","hash":{},"fn":this.program(8, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "  </tbody>\r\n</table>\r\n";
},"8":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "    <tr><td><a href=\"./trip.html?id="
    + escapeExpression(((helper = (helper = helpers.trip_id || (depth0 != null ? depth0.trip_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_id","hash":{},"data":data}) : helper)))
    + "\" class=\"success\">"
    + escapeExpression(((helper = (helper = helpers.tripname || (depth0 != null ? depth0.tripname : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tripname","hash":{},"data":data}) : helper)))
    + "</a> ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.creator_id : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</td></tr>\r\n";
},"9":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<a href=\"./trip_edit.html?id="
    + escapeExpression(((helper = (helper = helpers.trip_id || (depth0 != null ? depth0.trip_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"trip_id","hash":{},"data":data}) : helper)))
    + "\"><b>[Edit]</b></a>";
},"11":function(depth0,helpers,partials,data) {
  var stack1, buffer = "<div class=\"panel-body\" style=\"padding-top: 0px;\">\r\n  <br style=\"margin-top: 5px;\"></br>\r\n  <span class=\"label label-warning\">Have you ever been to?</span>\r\n</div>\r\n<table class=\"table\">\r\n  <thead></thead>\r\n  <tbody>\r\n";
  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.rec_locations : depth0), {"name":"each","hash":{},"fn":this.program(12, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    <tr><td><a href=\"./location_create.html\">+ Create New Location</a></td></tr>\r\n  </tbody>\r\n</table>\r\n";
},"12":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "    <tr><td><a href=\"./location.html?id="
    + escapeExpression(((helper = (helper = helpers.location_id || (depth0 != null ? depth0.location_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"location_id","hash":{},"data":data}) : helper)))
    + "\">"
    + escapeExpression(((helper = (helper = helpers.locationname || (depth0 != null ? depth0.locationname : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"locationname","hash":{},"data":data}) : helper)))
    + "</a></td></tr>\r\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, buffer = "";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.username : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
})();