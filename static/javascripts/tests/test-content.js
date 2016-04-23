describe('Dashboard Tests', function(){
  before('render Components', function() {

    this.DashboardRenderTree =  TestUtils.renderIntoDocument(
      <Page routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)
  });

  it("is Rendering <Page />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'mainDiv') != null);
  });
  it("is Rendering <SurveyDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'surveyDiv') != null);
  });
  it("is Rendering <Card />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'cardDiv') != null);
  });
  it("is Rendering <TitleSection />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'questionTitleDiv') != null);
  });
  it("is Rendering <TitleSurvey />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'surveyTitleDiv') != null);
  });
  it("is Rendering <Footer />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'footerDiv') != null);
  });
  it("is Rendering <Progress />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'progressDiv') != null);
  });
  it("is Rendering <PrevButton />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'prevButtonDiv') != null);
  });
  it("is Rendering <NextButton />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'nextButtonDiv') != null);
  });
  it("is Rendering <SubmitButton />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.DashboardRenderTree, 'submitButtonDiv') != null);
  });
});

describe('ResponseCard Tests', function(){
    
  before('render Components', function(){
    this.ResponseCardRenderTree =  TestUtils.renderIntoDocument(
      	<ResponseCard 
      		key = {0}
                questions={
		   [{"id" : "c0ea9fed-21b8-4280-8deb-37e198632bb1",
		     "options" : ["A","B","C","D"],
		     "response_format" : "multipleChoice",
		     "title" : "Test Question"	
		   }]
		}
                routes={
		   {"surveys": "/api/surveys",
		    "response": "/api/response",
		    "search": "/api/search",
		    "groups": "/api/groups",
		    "subscribe": "/api/subscribe",
		    "search": "/api/search"
		   }
		}
                surveyID= "Test Survey ID"
                department= "Test Department"
                creator= "Test Creator"
                isInstructor={false}
                surveyTitle= "Test Survey Title" />)
  });

  it("is Rendering <ResponseCard />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ResponseCardRenderTree, 'responseCardDiv') != null);
  }); 
  it("is Rendering <ChartDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ResponseCardRenderTree, 'chartDivDiv') != null);
  }); 
  it("is Rendering <ResponseFooter />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ResponseCardRenderTree, 'responseFooterDiv') != null);
  });  
});

describe('Profile Tests', function(){
  before('render Components', function() {
  
  this.ProfilePageRenderTree = TestUtils.renderIntoDocument(
    <ProfilePage routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)

  this.ProfileGroupsRenderTree = TestUtils.renderIntoDocument(
    <ProfileGroups routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)
  
  });

  it("is Rendering <ProfilePage />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ProfilePageRenderTree, 'profilePageDiv') != null);
  });
  it("is Rendering <ProfileGroups />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ProfileGroupsRenderTree, 'profileGroupsDiv') != null);
  });  
  it("is Rendering <SubscribedGroupDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ProfileGroupsRenderTree, 'subscribedGroupDiv') != null);
  });  
  it("is Rendering <PendingGroupDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.ProfileGroupsRenderTree, 'pendingGroupDiv') != null);
  });  
});

describe('Group Page Tests', function(){
  before('render Components', function(){
  
  this.GroupPageRenderTree = TestUtils.renderIntoDocument(    
    <GroupsPage routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)

  });

  it("is Rendering <GroupsPage />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.GroupPageRenderTree, 'groupsPageDiv') != null);
  });
  it("is Rendering <CreateGroup />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.GroupPageRenderTree, 'createGroupDiv') != null);
  });
  it("is Rendering <GroupMembers />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.GroupPageRenderTree, 'groupMembersDiv') != null);
  });    
  it("is Rendering <BrowseGroups />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.GroupPageRenderTree, 'browseGroupsDiv') != null);
  });
  it("is Rendering <GroupSearch />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.GroupPageRenderTree, 'groupSearchDiv') != null);
  });
  it("is Rendering <GroupList />", function(){
    assert(TestUtils.scryRenderedDOMComponentsWithClass(this.GroupPageRenderTree, 'groupListDiv') != null);
  });
});

describe('Surveys Page Tests', function(){
  before('render Components', function(){
  
  this.SurveysPageRenderTree = TestUtils.renderIntoDocument(    
    <SurveysPage routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)

  });

  it("is Rendering <SurveysPage />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'surveysPageDiv') != null);
  });
  it("is Rendering <TitleSection />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'questionTitleDiv') != null);
  });
  it("is Rendering <QuestionDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'questionDivDiv') != null);
  });
  it("is Rendering <Fields />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'fieldsDiv') != null);
  });
  it("is Rendering <OptionsDiv />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'optionsDivDiv') != null);
  });
  it("is Rendering <CheckboxQuestion />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'checkboxQuestionDiv') != null);
  });
  it("is Rendering <AddQuestion />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'addQuestionDiv') != null);
  });
  it("is Rendering <RemoveQuestion />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'removeQuestionDiv') != null);
  });
  it("is Rendering <FinishSurvey />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'finishSurveyDiv') != null);
  });
  it("is Rendering <SurveyTitleCreation />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'surveyTitleCreationDiv') != null);
  });
  it("is Rendering <SearchCard />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.SurveysPageRenderTree, 'searchCardDiv') != null);
  });
});

describe('Help Page Tests', function(){
  before('render Components', function(){
  
  this.HelpPageRenderTree = TestUtils.renderIntoDocument(    
    <HelpPage routesObject = {
     {"surveys": "/api/surveys",
      "response": "/api/response",
      "search": "/api/search",
      "groups": "/api/groups",
      "subscribe": "/api/subscribe",
      "search": "/api/search"}
     } />)

  });

  it("is Rendering <HelpPage />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.HelpPageRenderTree, 'helpPageDiv') != null);
  });
  it("is Rendering <GroupsHelp />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.HelpPageRenderTree, 'groupsHelpDiv') != null);
  });
  it("is Rendering <SurveysHelp />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.HelpPageRenderTree, 'surveysHelpDiv') != null);
  });
  it("is Rendering <Censorship />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.HelpPageRenderTree, 'censorshipDiv') != null);
  });
  it("is Rendering <InformationCollection />", function(){
    assert(TestUtils.findRenderedDOMComponentWithClass(this.HelpPageRenderTree, 'informationCollectionDiv') != null);
  });
});