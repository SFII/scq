var testQuestions = [
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: 1,
                type: "trueOrFalse",
                title: "Would you recommend this course?",
                options: ["Yes", "No"]
            }, {
                id: "asdasdad",
                type: "freeResponse",
                title: "What things should be improved?"
            }, {
                id: 2,
                type: "multipleChoice",
                title: "Did you enjoy the course?",
                options: ["Not at all", "It was an average course", "It was an excellent course"]
            },
            {
            id:"test",
            type:"rating",
            title: "How would you rate this course?"
            }
        ]
    },
    
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: "asdasdad",
                type: "freeResponse",
                title: "What did you not like about the course?"
            }, {
                id: 1,
                type: "trueOrFalse",
                title: "Will you take another course in the same field?",
                options: ["Yes", "No"]
            }, {
                id: 2,
                type: "trueOrFalse",
                title: "Was the grade policy fair?",
                options: ["Yes", "No"]
            }
        ]
    },
    
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: 1,
                type: "trueOrFalse",
                title: "Would you recommend this course?",
                options: ["Yes", "No"]
            }, {
                id: "asdasdad",
                type: "freeResponse",
                title: "What things should be improved?"
            }, {
                id: 2,
                type: "multipleChoice",
                title: "Did you enjoy the course?",
                options: ["Not at all", "It was an average course", "It was an excellent course"]
            }
        ]
    }
];
/*
* Page is the overall container that gets mounted into our HTML file
*/
var Page = React.createClass({
//loadPageJSON is the function we call whenever we want to call GET on the surveys endpoint
    loadPageJSON: function() {
    $.ajax({
    url: this.props.routes.surveys,
    type: 'GET',
    dataType: 'json',
    cache: true,
    success: function(data){
    //on success we set the state of Page to be equal to the JSON received
    this.setState({data: data});
    }.bind(this),
    error: function(xhr, status, err){
        console.error(this.props.routes.surveys, status, err.toString());
    }.bind(this)
    });
    },
    //This is where the initial loadPageJSON call happens, it happens when the React class is instantiated (Carlos we should put that 
    //initial fetch Sam showed you here)
    getInitialState: function() {
    this.loadPageJSON();
    return{data:[]};
    },
    //This is something we'll likely want to change, it calls loadPageJSON again once the component mounts, which doesn't really make sense, oops
    componentDidMount: function(){
        this.loadPageJSON();
    },
    
    //MainDiv is sent the data state as "pageJson" and the api routes json as "routes"
    render: function(){
      return (
        <div className="mdl-grid mdl-cell--12-col content">
        <MainDiv pageJson={this.state.data} routes={this.props.routes}/>
        </div>
        );
    }
});

/*
*
* MainDiv
* At this layer we separate each Survey into separate SurveyDiv objects
*/
var MainDiv = React.createClass({
    render: function() {
		if (!loggedIn()) {
		   return (<Welcome />);
		}
        routesObject=this.props.routes;
        //itemNodes is the set of mapped items (each one is a survey) and each is passed it's set of questions, routes, and other relevant information
        /*this is set to testQuestions.map until the GET works, if it's
        working switch it to this.props.pageJson and it should work */
        var itemNodes = this.props.pageJson.map(function (item) {
                return (
                <SurveyDiv 
                questions={item.questions}
                routes={routesObject}
                surveyID={item.surveyID}
                department={item.department}
                creator={item.creator}
                isInstructor={item.isInstructor}/>
                );
            });
        return (
        <div className="mainDiv ">
            {itemNodes}
        </div>
        );
    }
});
    
var SurveyDiv = React.createClass({
    //We want our Survey cards to disappear once submitted, so the getInitialState and removeCard functions provide a boolean
    //that we check before/while rendering
    getInitialState: function() {
        return{
            showCard: true
        };
    },  
    removeCard: function() {
        this.setState({showCard: false});
    },
    
    render: function() {
        //increasing the scope of the props, there has to be a better way to do this.
        var routesObject = this.props.routes;
        var removeCard = this.removeCard;
        var surveyID = this.props.surveyID;
        var department = this.props.department;
        var creator = this.props.creator;
        var isInstructor = this.props.isInstructor;
        //if showCard state is true, then we map the surveys questions onto cards, else we map nothing, pass all properties again.
        var itemSurvey = this.state.showCard ? this.props.questions.map(function (itemSurvey) {  
            return(
                <Card
                questionID ={itemSurvey.id}
                title={itemSurvey.title}
                options={itemSurvey.options}
                response_format={itemSurvey.response_format}
                routes={routesObject}
                removeHandler={removeCard}
                surveyID={surveyID}
                department={department}
                creator={creator}
                isInstructor={isInstructor}>
                </Card>
            );
            }) : '';
        return(
        <div className="surveyDiv">
            {itemSurvey}
        </div>
        );
    }
    });


function loggedIn() {
	return document.cookie.indexOf("user") > -1
}