/*
* Page is the overall container that gets mounted into our HTML file
*/
var Page = React.createClass({
    componentDidMount: function () {
        const unansweredSurveys = data.length
        const title = document.title
        const newTitle = title + " (" + unansweredSurveys +  ")"
        document.title = newTitle

        const header =  title + " - " + unansweredSurveys + " unanswered survey"
	if(test == false){
            $('.mdl-layout-title')[0].innerHTML = header + (unansweredSurveys != 1 ? "s" : "")
	}
    },

    //if we're not logged in we want to render a Welcome menu
    render: function(){
        /*data is a variable defined in dashboard.html as var data = {% raw survey_json %}
           which is a json of the unaswered_surveys list from the db, we map it out so each item
           is a survey that gets it's own SurveyDiv react component'*/
        var routesObject=this.props.routes;
        if (data.length == 0) {
            return (
                <div>
                  You don't have any open surveys right now. You can <a
                  href="/rawdump">view</a> survey results or <a
                  href="/surveys">create</a> your own survey using the bar on
                  the left.
                </div>
            )
        }
        var itemNodes = data.map(function (item) {
            return (
                <SurveyDiv
                    key = {item.id}
                    questions={item.questions}
                    routes={routesObject}
                    surveyID={item.id}
                    department={item.department}
                    creator={item.creator}
                    isInstructor={item.isInstructor}
                    surveyTitle={item.item_name}/>
            );
        });
        var answeredSurveys
        if (itemNodes.length < 10) {
            var ids = user_data[0].answered_surveys
            ids.length = (10 - itemNodes.length)
                answeredSurveys = ids.map(function(id, idx) {
                    return <ResponseCard surveyID={id} key={idx}/>
                });
        }
        //return the surveyDiv's in an mdl-grid with a SurveyCreationCard below it (This will probably change after Survey Creation is migrated)
        return (
            <div className="mdl-grid mdl-cell--12-col content">
              <div className="mainDiv">
                {itemNodes}
                {answeredSurveys}
              </div>
            </div>
        );
    }
});

var SurveyDiv = React.createClass({

    /* SurveyDiv contains the overarching json we're looking to submit through ajax as well as a secondary functionality that makes the card disappear after Submit is pressed
    getInitialState initializes our response json in it's state as well as other information we need to know to make everything work */
    getInitialState: function() {
        return({
                length: 0,
                showCard: true,
                iter: 0,
                responseSize: 0,
                response: {
                    survey_id: 0,
                    question_responses:[]
                },
                responded: false,
        });
    },

    componentDidMount: function() {
        this.setState({
            length: Object.keys(this.props.questions).length,
            response: {
                survey_id: this.props.surveyID,
                question_responses: []
            },
        });
    },

    //handler is called in footer.jsx, it receives data about the card that's currently being rendered updating the response state one last time before posting through ajax
    handleSurveySubmit: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        //iterate through our question_responses looking to see if the question has previously been answered before, if so we replace the previous answer state by splicing and pushing
        var length = Object.keys(response.question_responses).length;
        for(var i=length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }
        response.question_responses.push(question_responses_object);
        this.setState({response: response});

        $.ajax({
            url: this.props.routes.response,
			contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(response),
            success: function(data){
                this.setState({responded: true});
            }.bind(this),
			error: function(xhr, status,err){
                console.log(this.state.response);
				console.error("/api/response", status, err.toString());
			}.bind(this)
        });
    },

    //called in the ajax success function, sets showCard to false which will make the SurveyDiv stop rendering
    removeCard: function() {
        this.setState({showCard: false});
    },

    /*nextQuestion and prevQuestion have similar functionality to submit, just without the ajax, we check to see if it's been previously answered
    with a for loop looking to match on questionID and then splicing and pushing if we match (otherwise just pushing) but we also increment or decrement
    this.state.iter*/
    nextQuestion: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for(var i=length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({response: response});
        this.setState({responseSize: Object.keys(this.state.response.question_responses).length});

        var iter = this.state.iter;

        this.setState({iter: iter + 1});
    },

    prevQuestion: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for(var i = length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({response: response});
        this.setState({responseSize: Object.keys(this.state.response.question_responses).length});

        var iter = this.state.iter;


        this.setState({iter: iter - 1});

    },

    render: function() {
        if (this.state.responded) {
            return (
                <ResponseCard {...this.props}/>
            )
        } else
        /*if showCard state is true, then we render <Card>, questionID, title, options, response_format vary depending on this.state.iter
        which is manipulated by the previous and next buttons so we can have all the survey's questions on one card.*/
        if(this.state.showCard == true) {
            return(
            <div className="surveyDiv">
                <Card
                routes={this.props.routes}
                questionNum={this.state.iter}
                questionID = {this.props.questions[this.state.iter].id}
                responseSize = {this.state.responseSize}
                numQuestions={Object.keys(this.props.questions).length}
                title={this.props.questions[this.state.iter].title}
                options={this.props.questions[this.state.iter].options}
                response_format={this.props.questions[this.state.iter].response_format}
                surveyID={this.props.surveyID}
                department={this.props.department}
                creator={this.props.creator}
                isInstructor={this.props.isInstructor}
                removeHandler={this.removeCard}
                nextHandler={this.nextQuestion}
                prevHandler={this.prevQuestion}
                onSubmit={this.handleSurveySubmit}
                responseState = {this.state.response.question_responses}
                surveyTitle = {this.props.surveyTitle}/>
            </div>
            );
        }
        else{
        return(
        <div></div>
        );
        }
    }
    });


function loggedIn() {
	return document.cookie.indexOf("user") > -1
}
