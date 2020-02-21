




    

<section style="z-index:100000;background:gray;">

    <input class="button_declencheur" type="button" id="response" onclick="phase1()">
    <input class="button_declencheur" type="button" id="response2" onclick="phase2(0)">
    <input class="button_declencheur" type="button" id="response3" onclick="phase3()">

    <div id="visionnage">

        <div id="uploding_camera" style="display:none;">
            {% include "home_composition/sections/section3/upload/upload.html" %}
        </div>


        <div id="loading_eyes_section" style="display:none;">

            <img src="static/home_composition/section3/images/loading_s3_p2_p3.gif" id="loading">
            <p>L O A D I N G ... <br>
                Nous chargeons la vidéo, prenez le temps de visiter notre site, nous vous ferons signe
            </p>
        </div>


    </div>








    <div id="to_camera" style="width:100%;height:100%;">

            <input type="button" value="croix" onclick="quit_webcam_page_eye_apli()" id="croix_webcam" style="border:2px solid red;">
            <input type="button" value="croix2" onclick="end_download()" id="end_download" style="display:none;">


        <div id="buttons">



            <button class="clio_button" id="btn-start-recording">Recording</button>

            <button class="clio_button" id="btn-pause-recording"
                 style="display:none;">Pause</button>

            <button class="clio_button" id="save-to-disk">Save</button>
        </div>


        <div style="margin-top: 10px;" id="recording-player"></div>


    </div>






        



 




    <div id="parameter_webcam_page_eye">









        <p id="ask_webcam">

            <strong><span style="color:red;">Important :</span></strong> Nous vous prions de bien vouloir essayer<br>
            la caméra avant de faire votre enregistrement avec <strong>les différents encodages</strong>. <br><br>

            Votre navigateur est : <strong><span id="navigator_span"></span></strong>
        </p>




        <h1>Eyes detectors</h1>
        <p>Choix applications</p>

        <ul id="applation_eye">
            <li class="appli_eyes">choix appli</li>
            <li class="appli_eyes" onclick="eyes_application_choice('site')">Eyes tracking visite de site web</li>
            <li class="appli_eyes" onclick="eyes_application_choice('accessoire')">Des accesoires pour votre figure</li>
            <li class="appli_eyes" onclick="eyes_application_choice('dormir')">Ne pas dormir au volant !</li>
            <li class="appli_eyes" onclick="eyes_application_choice('tracking')">eyes detector !</li>
            <li class="appli_eyes" onclick="eyes_application_choice('experience')">notre experience sociale</li>
        </ul>









        <p id="recommandation">
            <span>Recommandation: De face, une bonne qualité de caméra. Yeux bien visible.</span>
        </p>



        <p>tu te prend en video, tu nous la fais télécharger et c'est parti !</p>

        <button class="clio_button" id="Button_eye_application" onclick="to_video()">J'essaie la vidéo</button>


















    </div>


    <div style="display: none">
        <input type="checkbox" id="chk-fixSeeking" style="margin:0;width:auto;display:none;" title="">
        <label for="chk-fixSeeking" style="font-size: 15px;margin:0;width: auto;
        cursor: pointer;-webkit-user-select:none;user-select:none;"
        title="Fix video seeking issues?"></label>
    </div>


  

<section>















<style>
.button_declencheur{
    display:none;
}
#response{
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
}
#loading_eyes_section{
    margin-top:10%;
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
}
#loading{
    width:10%;
}
#visionnage{
    width:100%;
    height:100%;
    display:block;
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
}
.appli_eyes:hover{
    color:green;
    cursor:pointer;
}
#to_application_to_camera{
    z-index:300;
    position:absolute;
    display:none;
    opacity:0;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
}
#to_camera{
    z-index:500;
    position:absolute;
    opacity:0;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
    display:none;
}
#parameter_webcam_page_eye{
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
    z-index:1;
}
#Button_eye_application{
    font-size:1.5em;
}
#applation_eye{
    list-style:none;
    text-align:center;
    margin-left:38%;
}

#recommandation{
}
#aplications_eyes{
    position:relative;
    text-align:center;
}
#ask_webcam{
    text-align:left;
    padding-top:1%;
    z-index:1;
    position:relative;
    height:100px;
}
#select1{
    background:gray;
    outline: 0;
    border:none;
    float:left;
    height:100px;
    overflow-y:hidden;
    position:relative;
    z-index:10;
}
#icon_recording{
    width:50px;
    height:50px;
    float:left;
    position:relative;
    padding-left:5px;
    margin-top:25px;
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
}
#select2{
    background:gray;
    outline: 0;
    border:none;
    float:left;
    padding-left:5%;
    height:100px;
    overflow-y:hidden;
    position:relative;
    z-index:10;
}
#icon_recording2{
    width:50px;
    height:50px;
    float:left;
    position:relative;
    padding-left:5px;
    margin-top:25px;
    opacity:1;
    -webkit-transition: opacity 2s;
    -moz-transition: opacity 2s;
    -o-transition: opacity 2s;
    transition: opacity 2s;
    padding-right:5%;
}

#navigator_ids{
    text-align:left;
}
.clio_button {
   color: #FFFFFF !important;
   position: relative;
   text-transform: initial !important;
   font-weight: 500 !important;
   z-index: 0;
   overflow: hidden !important;
   transition: transform 0s !important;
   font-family: Arial;
   border:none;
   outline: 0;
}
.clio_button:hover {
    color: #FFFFFF;
}
.clio_button::before, .clio_button::after {
   content: "";
   position: absolute;
   width: 100%;
   height: 100%;
   top: 0;
   transition: left 0.6s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.clio_button::before {
   background-color: #294C6B;
   z-index: -1;
   left: 0;
}
.clio_button::after {
   background-color: black;
   z-index: -1;
   left: 100%;
}
.clio_button:hover::before {
   left: -100%;
}
.clio_button:hover::after {
   left: 0;
}
.clio_button [class^="clio-"]::before {
    vertical-align: text-bottom;
}
.clio_button:active {
    transform: translateY(-2px);
}

#buttons{
    width:100%;
    margin-top:1%;
}
#btn-start-recording{
    width:12%;
    height:5em;
    border-radius:4px;
    border:1px solid blue;
    z-index:1000000000000;
}
#btn-pause-recording{
    width:12%;
    height:5em;
    border-radius:4px;
    border:1px solid blue;
}
#save-to-disk{
    height:5em;
    width:12%;
    border-radius:4px;
    border:1px solid blue;
    z-index:1000000000000;
}

select {
    border: 1px solid #d9d9d9;
    border-radius: 1px;
    height: 50px;
    margin-left: 1em;
    margin-right: -5px;
    padding: 1.1em;
    vertical-align: 6px;

}

.media-container, .media-container * {
    margin: 0;
    padding: 0;
    -webkit-user-select: none;
    -moz-user-select: none;
    -o-user-select: none;
    user-select: none;
}

.media-container, .media-container * {
    -moz-transition: all .5s ease-in-out;
    -ms-transition: all .5s ease-in-out;
    -o-transition: all .5s ease-in-out;
    -webkit-transition: all .5s ease-in-out;
    transition: all .5s ease-in-out;
}

.media-container {
    width: 50%;
    display: inline-block;
    border-radius: 4px;
    overflow: hidden;
    vertical-align: top;
    border:1px solid gray;
    outline: 10px solid black;
    background-image: url("/static/home_composition/section3/images/webcam_baground.jpg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    margin-top:10px;

    
}

.media-controls, .volume-control {
    margin-top: 2px;
    position: absolute;
    margin-left: 5px;
    z-index: 100;
    opacity: 0;
    border:1px solid gray;
}

.media-box video {
    width: 100%;
    vertical-align: top;
    object-fit: fill;
    

}


</style>
