var GroupsPage = React.createClass({
  render: function() {
    return (
      <div className="groupsPageDiv">
        <div>
          <CreateGroup/>
          <BrowseGroups/>
        </div>
      </div>
    );
  }
});

var CreateGroup = React.createClass({
  render: function() {
    var style = {
      marginTop: "5px",
      marginBottom: "5px"
    };

    return (
      <div style={style} className="createGroupDiv">
        <h3>Create a group</h3>
        <div className="mdl-grid">
          <div className="mdl-cell mdl-cell--1-col">
          </div>
          <div className="mdl-cell mdl-cell--11-col">
            <form action="/api/groups" method="POST">
              <div className="mdl-textfield
                mdl-js-textfield
                mdl-textfield--floating-label">
                <input style={{fontSize: "24px"}}
                  type="text" name="groupname"
                  className="mdl-textfield__input"></input>
                <label className="mdl-textfield__label"
                  htmlFor="groupname">Group name</label>
              </div>
              <GroupMembers/>
              <input className="mdl-button
                mdl-js-button
                mdl-button--raised
                mdl-js-ripple-effect"
                type="submit" value="Create"></input>
            </form>
          </div>
        </div>
      </div>
    );
  }
});

var GroupMembers = React.createClass({
  getInitialState: function() {
    return ({
      members: [user_data[0].username]
    });
  },

  newMember: function(e) {
    this.setState(function(state) {
      state.members.push(e.target.value);
    });
  },
  render: function() {
    var memberlist = [];
    var count = this.state.members.length;
    var element = function(key, user) {
      return <div key={key}>
        <div className="mdl-textfield" key={i}>
          <input type="text"
            name="members"
            className="mdl-textfield__input memberlist"
            defaultValue={user} >
          </input>
        </div>
      </div>;
    };
    
    memberlist.push(
    <div key={0}>
        <div className="mdl-textfield" key={0}>
          <input type="text"
            name="members"
            className="mdl-textfield__input memberlist"
            defaultValue={this.state.members[0]}
            readOnly>
          </input>
        </div>
    </div>
    );
    
    for (var i = 1; i < count; i++) {
      memberlist.push(element(i, this.state.members[i]));
    }
    memberlist.push(
      <div className="mdl-textfield" key={i}>
        <input type="text"
          name="person"
          className="mdl-textfield__input memberlist"
          defaultValue={""}
          onChange={this.newMember}>
        </input></div>
      );
      return (
        <div className="groupMembersDiv">
          <h4>Members</h4>
          Add initial members here, but anyone can join
          {memberlist}
        </div>
      );
    }
  });

  var BrowseGroups = React.createClass({
    findGroups: function() {
      const outer_this = this;
      $.ajax({
        url: '/api/search'
      })
      .then(function(data) {
        data = JSON.parse(data);
        outer_this.setState({
          relevant: data['relevant'],
          popular: data['popular']
        });
      });
    },

    componentDidMount: function() {
      if(test == false){
        this.findGroups();
      }
      else{
        this.setState({ 
	  relevant: ['relevantGroup1'],
	  popular: ['relevantGroup2']
	});
      }
    },

    getInitialState: function() {
      return ({
        search: "",
        relevant: [],
        popular: [],
        searchResults: [],
        subscribed: user_data[0].subscribed_groups
      });
    },

    handleChange: function(event) {
      const query = event.target.value;
      const groupQuery = {
        searchstring: query,
        search_type: 'Group',
        requestedfields: ['id']
      };

      $.ajax({
        url: '/api/search',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(groupQuery)
      })
      .then(data => {
        data = JSON.parse(data)
        .map(d => d.id);
        this.setState({
          searchResults: data
        });
      });
      this.setState({
        search: query
      });
    },

    subscribe: function(groupID) {
      const data = {
        "id": groupID,
        "action": "sub"
      };

      $.ajax({
        url: '/api/subscribe',
        data: JSON.stringify(data),
        type: 'POST'
      })
      .then(() => {
        this.setState({
          subscribed: this.state.subscribed + groupID
        });
      });
    },

    render: function() {
      var moreGroups = "";
      const groupList = groups =>
      < GroupList subbed = {
          this.state.subscribed
        }
        subscribe = {
          this.subscribe
        }
        groups = {
          groups
        } > < /GroupList>;
        if (this.state.search == "") {
          moreGroups =
          <div>
            <h4>Popular groups</h4>
            {groupList(this.state.popular)}
            <h4>Groups you might be interested in</h4>
            {groupList(this.state.relevant)}
          </div>;
        } else {
          moreGroups =
          <div>
            <h4>Search results</h4>
            {groupList(this.state.searchResults)}
          </div>;
        }
        return (
          <div className="browseGroupsDiv">
            <h3>Browse groups</h3>
            <div className="mdl-grid">
              <div className="mdl-cell mdl-cell--1-col"></div>
              <div className="mdl-cell mdl-cell--11-col">
                <GroupSearch
                  search={this.state.search}
                  handleChange={this.handleChange}
                  results={this.state.searchResults}>
                </GroupSearch>
                {moreGroups}
              </div>
            </div>
          </div>
        );
      }
    });

    var GroupSearch = React.createClass({
      render: function() {
        return (
          //style={{display: "inline"}}
          <span
            className="mdl-textfield 
	    groupSearchDiv
            mdl-js-textfield
            mdl-textfield--floating-label">
            <input style={{fontSize: "24px"}}
              type="text" name="search"
              className="mdl-textfield__input"
              value={this.props.search}
              onChange={this.props.handleChange}></input>
            <label className="mdl-textfield__label"
              htmlFor="search">Search</label>
          </span>
        );
      }
    });

    var GroupList = React.createClass({
      render: function() {
        const groups = this.props.groups.map(
          (val, idx) => {
            var disabled = this.props.subbed.indexOf(val) >= 0;
            var input =
            <input
              className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
              type="submit"
              onClick={() => this.props.subscribe(val)}
              disabled={disabled}
              value="Subscribe">
            </input>;
            return <div style={{marginBottom: "20px"}}
              key={idx}>
              {input}
              <h5 style={{display: "inline",
                verticalAlign: "text-bottom",
                marginLeft: "10px"}}>
                {val}</h5>
            </div>;
          });
          return (
            <div className="groupListDiv">{groups}</div>
          );
        }
      });
