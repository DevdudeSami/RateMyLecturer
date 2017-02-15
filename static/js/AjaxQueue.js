var isProcessing = false;
var ajaxQueue = [];
function nextAjaxRequest() {
    isProcessing = false;
    if(typeof ajaxQueue[0] !== 'undefined') {
        next = ajaxQueue[0];
        ajaxQueue.splice(0, 1);
        if(typeof next.withArgs !== 'undefined' && next.withArgs) {
            next.call.apply(this, next.args);
        } else {
            next();
        }
    }
}