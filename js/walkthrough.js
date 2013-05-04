        //Temporary Javascript for storytelling. Will be moved to its own file when done.
    //storyArray. First is text, then languages used (Array), then times (Array, [start, end])
    var currentStory = 0;
    var storyArray = [];
storyArray[0] = new Array('Data Visualization Created for CS171 <br> by Ryan Mitchell and Yuki Yamada', new Array('en'), new Array(23, 0));


storyArray[1] = new Array('Wikipedia edit histories visualized over space and time provide fascinating insights into cultural, geographic, and political phenomena: languages that have spread beyond their sovereign boundaries, and those that have remained isolated; migratory patterns of language speakers throughout the world; geographic and political divisions; and finally, due to Wikipedia\'s living on the internet, the unavoidable fact that much of the world remains unconnected to the internet.', new Array('en'), new Array(23,0));

    storyArray[2] = new Array('Waray Waray is a Philippine language. Although few edits originate from within the Phillippine Islands, there is a dense cluster of edits located in Southern California. As it turns out, there is a very large Filipino population in LA, with estimates as high as 500,000 native Filipinos living there.', new Array('war'), new Array(23, 0));

    storyArray[3] = new Array('Despite the best efforts of many Soviet Bloc countries to replace Russian with their native tongue after the fall of communism, Russian still remains a commonly spoken language in many of these countries. The areas from which Russian Wikipedia edits originate create a ghostly outline of the fallen USSR.', new Array('ru'), new Array(23, 0));

storyArray[4] = new Array('There are many countries around the world that speak French, however the main ones highlighted in our visualization appear to be France and French Canada. Although many African countries (Congo, Benin, Niger, etc.) have French as a national language, the lack of internet access prevents them from appearing more prominently in the visualization.', new Array('fr'), new Array(23, 0));


    storyArray[5] = new Array('Although the United States tends to dominate when it comes to English Wikipedia edits, the Brits sneak up on us while we\'re sleeping. During the hours of 8:00 to 12:00 UTC there more English edits made from the United Kingdom than the entire United States (this is 4am-8am Boston time)', new Array('en'), new Array(12, 8));


storyArray[6] = new Array('China has a population over 10 times as large as that of Japan, but the Chinese Wikipedia has far fewer edits due to the lack of unrestricted internet access.', new Array('ja', 'zh'), new Array(23, 0));


storyArray[7] = new Array('Japanese is one of the most isolated of the languages, with nearly no Japanese edits made outside of Japan. This may be because of compulsory English education in Japan, and the general tendency for Japanese to speak multiple languages. When Japanese emigrate, they tend to speak the language of their new country.', ['ja'], [23, 0]);

storyArray[8] = new Array('Wikipedia is more than just an encyclopedia. It embodies the spirit of the Internet age; the free, open spread of knowledge; the globalization of language and cultural ideas. Because Wikipedia is open to edits from anywhere in the world, it also acts as a nexus for a global community to come together and share in the creation of a singular body of knowledge.', new Array('en','de','fr','nl','it','ru','es','pl','sv','ja','pt','zh','vi','uk','ca','no','ceb','fi','war','cs'), new Array(23, 0));


    $('#prevButton').click(function(){
        currentStory = (currentStory-1) % storyArray.length;
        console.log("current story is: "+currentStory);
        reset(storyArray[currentStory]);
    });

    $('#nextButton').click(function(){
        //Change stuff here
        //Update story Array index
         console.log("current story is: "+currentStory);

        currentStory = (currentStory+1) % storyArray.length;
        reset(storyArray[currentStory]);
    });

    function reset(story){
        console.log("Setting to Array values");
        $('.presetText').html(story[0]);
        $('input.language').prop('checked', false);
        
        console.log("Setting presets to languages: ");
        console.log(story[1]);
        var newLangArray = [];
        for(var i = 0; i < story[1].length; i++){
            console.log("Language is: "+story[1][i]);
            //Check boxes and trigger event with jQuery for each language
            $('#'+story[1][i]+'Toggle').trigger('click');
            $('#'+story[1][i]+'Toggle').prop('checked', true);
            newLangArray.push(story[1][i]);
        }

            passArgs([story[2][1], story[2][0]], newLangArray);
            //set the sliders to the correct positions
            console.log("Moving sliders");
            moveSliders(story[2][0], story[2][1]);
    }
