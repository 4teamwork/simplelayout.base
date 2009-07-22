var simplelayout = new Object();
simplelayout.edit_mode = 0

simplelayout.toggleEditMode = function(){
    
	var controls = cssQuery('.sl-controls');
	
	for(var i=0; i<controls.length; i++) {
	    var current_display = controls[i].style.display;
   		current_display == 'block' ? controls[i].style.display = 'none' : controls[i].style.display = 'block';
        }

    var blocks = jq('.BlockOverallWrapper'); 
    blocks.toggleClass("blockHighlight");
    var slots = jq('.simplelayout-content [id*=slot]').toggleClass('highlightBorder');

    var imgblocks = jq('.BlockOverallWrapper.image');
    for (var b=0;b<imgblocks.length;b++) {
        var query_wrapper = '#'+imgblocks[b].id + ' .sl-img-wrapper';
        var width = jq(query_wrapper).width();
        
        var query_controls = '#'+imgblocks[b].id + ' .sl-controls';
        var controls_el = jq(query_controls)[0];
        controls_el.style.width = width+'px';
        
        }
    
    
    
    var $view = jq('#contentview-view');
    $view.toggleClass("selected");
    var $edit = jq('#contentview-edit-toggle');
    $edit.toggleClass("selected");
    setTimeout(function(){
        jq(".simplelayout-content").trigger("toggleeditmode");
    }, 1);
}


jq(function(){
   if(simplelayout.force_edit_mode)
        simplelayout.toggleEditMode()
});


simplelayout.showEditModeButton = function(){
var sltoggle = document.getElementById('document-action-togglesledit');
	if (sltoggle){
		sltoggle.style.display = 'inline';
	}
}


function alignBlockToGridAction(){

    var containers = jq('.twocolumn');
    var left = jq('.BlockOverallWrapper',containers.get(0))
    var right = jq('.BlockOverallWrapper',containers.get(1))
    iterate = (left.length > right.length) ? left.length : right.length;
    var all_left_blocks = [];
    var all_right_blocks = [];
    var all_uids = [];  
    
    for (var i=0;i <= iterate;i++){
        var left_block = left[i];
        var right_block = right[i];
        var left_height = 0;
        var right_height = 0;

        if (typeof(left_block) != 'undefined'){
            left_block_content = jq('.simplelayout-block-wrapper',left_block);
            left_block_content.css('height','');
            left_height = left_block_content.height();
            
        }

        if  (typeof(right_block) != 'undefined'){
            right_block_content = jq('.simplelayout-block-wrapper',right_block);
            right_block_content.css('height','');
            right_height = right_block_content.height();
            

        }
        
        
        
        if ((left_height > 0 && right_height > 0) && (parseInt(simplelayout.align_to_grid)==1)) {
            if (true){
                var master_height = (left_height > right_height) ? left_height : right_height;
                master_height_in_em = jq(master_height).toEm();
                
                left_block_content.css('height',master_height_in_em);
                all_left_blocks[i] = [jq(left_block).attr('id'), master_height_in_em];
                
                right_block_content.css('height',master_height_in_em);
                all_right_blocks[i] = [jq(right_block).attr('id'), master_height_in_em];
                
            }
        }
    }
    
    jq('.BlockOverallWrapper').each(function(i,o){
        all_uids[i] = jq(o).attr('id');
    });
    
    //reset all others (if block moved to onecolumn slot)
    jq('.onecolumn .BlockOverallWrapper').css('height','');
    
    jq.post(getBaseUrl()+'block_manipulation/setBlockHeights',{'uids:list':all_uids,'left:list':all_left_blocks, 'right:list':all_right_blocks}, function(data){});
}


jq(function(){
    jq(".simplelayout-content").bind("actionsloaded",function(e){
        jq('#alignallblocks').bind('click',function(e){
        e.stopPropagation();
        e.preventDefault();

        
        simplelayout.align_to_grid = parseInt(simplelayout.align_to_grid)==0 ? 1 : 0;
        jq.get(getBaseUrl()+'simplelayout/toggle_align_to_grid',{'new_value':simplelayout.align_to_grid}, function(data){
            jq('#alignallblocks').load(getBaseUrl()+'sl_controls/ToggleGridLayoutText');
        });

        alignBlockToGridAction();
        });
    });
    
    //jq(".simplelayout-content").bind("afterReorder", alignBlockToGridAction); 

});

