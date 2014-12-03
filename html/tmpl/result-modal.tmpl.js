(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['result-modal.tmpl'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, lambda=this.lambda;
  return "<div class=\"modal fade\" tabindex=\"-1\" role=\"dialog\" id=\""
    + escapeExpression(((helper = (helper = helpers.modal_id || (depth0 != null ? depth0.modal_id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"modal_id","hash":{},"data":data}) : helper)))
    + "\" aria-hidden=\"true\">\r\n    <div class=\"modal-dialog modal-sm\">\r\n        <div class=\"modal-content\">\r\n            <div class=\"text-center\" style=\"padding: 10px;\"><b>"
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.result : depth0)) != null ? stack1.status : stack1), depth0))
    + "</b>: "
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.result : depth0)) != null ? stack1.message : stack1), depth0))
    + "</div>\r\n        </div>\r\n    </div>\r\n</div>";
},"useData":true});
})();