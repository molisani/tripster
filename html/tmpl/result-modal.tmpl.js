(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['result-modal.tmpl'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<div class=\"modal fade\" tabindex=\"-1\" role=\"dialog\" id=\"result-modal\">\r\n    <div class=\"modal-dialog modal-sm\">\r\n        <div class=\"modal-content\">\r\n            <div class=\"text-center\" style=\"padding: 10px;\">"
    + escapeExpression(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"message","hash":{},"data":data}) : helper)))
    + "</div>\r\n        </div>\r\n    </div>\r\n</div>";
},"useData":true});
})();