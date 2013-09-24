simplelayout.alignBlockToGridAction = function(){

    var containers = $('.twocolumn');
    var left = $('.BlockOverallWrapper',containers.get(0));
    var right = $('.BlockOverallWrapper',containers.get(1));
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
            var left_block_content = $('.simplelayout-block-wrapper',left_block);
            var left_block_controls = $('.sl-controls',left_block);
            left_block_content.css('height','');
            // calc block height, to prevent problems with float, we take the overallblock height
            // includes the controls area, then overallblockheight - controlsheight
            left_height = $(left_block).height();
        }

        if  (typeof(right_block) != 'undefined'){
            var right_block_content = $('.simplelayout-block-wrapper',right_block);
            var right_block_controls = $('.sl-controls',right_block);
            right_block_content.css('height','');
            right_height = $(right_block).height();
        }


        if ((left_height > 0 && right_height > 0) && (parseInt(simplelayout.align_to_grid)==1)) {
            if (true){
                var master_height = (left_height > right_height) ? left_height : right_height;


                left_block_content.css('height', master_height);
                all_left_blocks[i] = [$(left_block).attr('id'), master_height];

                right_block_content.css('height', master_height);
                all_right_blocks[i] = [$(right_block).attr('id'), master_height];

            }
        }
    }

    $('.BlockOverallWrapper').each(function(i,o){
        all_uids[i] = $(o).attr('id');
    });

    //reset all others (if block moved to onecolumn slot)
    $('.onecolumn .BlockOverallWrapper').css('height','');
    $.post(getBaseUrl()+'block_manipulation/setBlockHeights',{'uids:list':all_uids,'left:list':all_left_blocks, 'right:list':all_right_blocks});
};


jQuery(function($){
    //$(".simplelayout-content").bind("actionsloaded",function(e){
        $('#alignallblocks').live('click',function(e){
        e.stopPropagation();
        e.preventDefault();

        simplelayout.align_to_grid = parseInt(simplelayout.align_to_grid)==0 ? 1 : 0;
        $.get(getBaseUrl()+'simplelayout/toggle_align_to_grid',{'new_value':simplelayout.align_to_grid}, function(data){
            $('#alignallblocks').load(getBaseUrl()+'sl_controls/ToggleGridLayoutText');
        });

        simplelayout.alignBlockToGridAction();
        });
    //});

    //$(".simplelayout-content").bind("afterReorder", alignBlockToGridAction);

});

