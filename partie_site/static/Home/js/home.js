//SCROLL SECTION

//We recuperate current position on scrolling.
function current_position(){
    var current_position = $(window).scrollTop()
    return current_position
};


//We recuperate position in Y of our sections list.
SECTIONS = ["#1", "#2", "#3", "#4", "#5"]
function recuperate_element_position(){

    positions = []
    for (var i = 0; i < SECTIONS.length; i ++){

        //position of sections
        var localisation = jQuery(SECTIONS[i]).offset().top;
        positions.push(localisation)
    };
    return positions
};



//Compare current position with section position.
function on_scroll(positions, current_position){


    //We all sections position
    var minimum_index = 100000
    var indexage = 0

    for (var index = 0; index < positions.length; index ++){

        difference = Math.abs(positions[index] - current_position);
        console.log("diff", difference, index)
        if (difference < minimum_index){
            indexage = index;
            minimum_index = difference;
        };
    };

    console.log(indexage);
    return indexage
};


//When user scroll we recuperate the min index for scroll smooth.
$( window ).scroll(function() {

    positions = recuperate_element_position();

    current_pos = current_position()
    console.log(positions, current_pos)

    indexage = on_scroll(positions, current_pos)
    console.log("le plus proche est :", indexage)

});
