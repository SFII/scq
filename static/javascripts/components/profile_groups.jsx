var ProfileGroups = React.createClass({
    getInitialState: function(){
        return({
            currentGroups: [],
            pendingGroups: user_data[0].pending_groups,
        });
    },

    subscribeGroup: function(groupID){
        var subJSON = {
            "id": groupID,
            "action": "sub"
        }
        console.log(subJSON);
        $.ajax({
            url: this.props.routes.subscribe,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(subJSON),
            success: function(data){
                this.refreshData();
            }.bind(this),
            error: function(xhr, status,err){
                console.log('error');
            }.bind(this)
        });
    },

    unsubscribeGroup: function(groupID){
        var unsubJSON = {
            "id": groupID,
            "action": "unsub"
        }
        console.log(unsubJSON);
        $.ajax({
            url: this.props.routes.subscribe,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(unsubJSON),
            success: function(data){
                this.refreshData();
            }.bind(this),
            error: function(xhr, status,err){
                console.log('error');
            }.bind(this)
        });
    },

    removePendingGroup: function(groupID){
        var removeJSON = {
            "id": groupID,
            "action": "remove_pending"
        }
        console.log(removeJSON);
        $.ajax({
            url: this.props.routes.subscribe,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(removeJSON),
            success: function(data){
                this.refreshDataPending();
            }.bind(this),
            error: function(xhr, status,err){
                console.log('error');
            }.bind(this)
        });
    },

    refreshData: function(){
        $.ajax({
                url: this.props.routes.groups,
                type: 'GET',
                dataType: "json",
                success: function(data){
                    var currentGroups = this.state.currentGroups;
                    currentGroups = data;
                    console.log('success');
                    this.setState({
                        currentGroups: data,
                    })
                }.bind(this),
                error: function(xhr, status,err){
                    console.log('error');
                }.bind(this)
        });
    },

    refreshDataPending: function(){
        $.ajax({
                url: this.props.routes.subscribe,
                type: 'GET',
                dataType: "json",
                success: function(data){
                    var pendingGroups = this.state.pendingGroups;
                    pendingGroups = data;
                    this.setState({
                        pendingGroups: data,
                    })
                }.bind(this),
                error: function(xhr, status,err){
                    console.log('error');
                }.bind(this)
        });
    },

    componentDidMount: function(){
	if(test == false){
		$.ajax({
		    url: this.props.routes.groups,
		    type: 'GET',
		    dataType: "json",
		    success: function (data) {
		        var currentGroups = this.state.currentGroups;
		        currentGroups = data;
		        this.setState({
		            currentGroups: data
		        });
		    }.bind(this),
		    error: function (xhr, status, err) {
		        console.log('error');
		    }.bind(this)
		});

		$.ajax({
		        url: this.props.routes.subscribe,
		        type: 'GET',
		        dataType: "json",
		        success: function(data){
		            var pendingGroups = this.state.pendingGroups;
		            pendingGroups = data;
		            this.setState({
		                pendingGroups: data,
		            })
		        }.bind(this),
		        error: function(xhr, status,err){
		            console.log('error');
		        }.bind(this)
		});
        }
	else{
		console.log(test)
		this.setState({ 
			currentGroups: ["TestSubscribedGroup"]
		});
	}
    },

    render: function(){

      var renderedGroups = this.state.currentGroups.map((group,i) => {
      if(this.state.currentGroups.length > 0){
        return (
        <SubscribedGroupDiv key={group.id} unsubscribeGroup={this.unsubscribeGroup} groupID = {group}/>
        )
      }
      else{
          return (
          <div key={group.id}></div>
        )
      }
      });

      var renderedPendingGroups = this.state.pendingGroups.map((group,i) => {
      if(this.state.pendingGroups.length > 0){
        return (
        <PendingGroupDiv key={group.id} subscribeGroup={this.subscribeGroup} removePendingGroup={this.removePendingGroup} groupID = {group}/>
        )
      }
      else{
          return (
          <div key={group.id}></div>
        )
      }
      });

      return(
          <div className="profileGroupsDiv mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
              <div className="mdl-card__title mdl-card--expand mdl-color--primary">
                <h2 className="mdl-card__title-text white_text"> My Groups </h2>
              </div>
              <div className="mdl-cell mdl-cell--12-col">
                <ul className= "mdl-list">
                    {renderedGroups}
                </ul>
              </div>
              <div className="mdl-card__title mdl-card--expand mdl-color--primary">
                <h2 className="mdl-card__title-text white_text"> Pending Groups </h2>
              </div>
              <div className="mdl-cell mdl-cell--12-col">
                <ul className= "mdl-list">
                    {renderedPendingGroups}
                </ul>
              </div>
          </div>
      );
    }
});

var SubscribedGroupDiv = React.createClass({

    clickHandler: function(){
        var id = this.props.groupID;
        this.props.unsubscribeGroup(id);
    },

    render: function(){
      var li_key = this.props.groupID + "." + "li";
      var span_key = this.props.groupID + "." + "span";
      var i_key = this.props.groupID + "." + "i";
      var i_key2 = this.props.groupID + "." + "i2";
      var a_key = this.props.groupID + "." + "a";
      var ul_key = this.props.groupID + "." + "ul";
        return(
            <li className="subscribedGroupDiv mdl-list__item" key={li_key}>
                <span className="groupListItem mdl-list__item-primary-content" key={span_key}>
                    <i className="groupListItem material-icons" key={i_key}>group</i>
                    {this.props.groupID}
                </span>
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onClick={this.clickHandler}>
                Unsubscribe
          </button>
            </li>
        )
    }
});

var PendingGroupDiv = React.createClass({

    clickSub: function(){
        var id = this.props.groupID;
        this.props.subscribeGroup(id);
        this.props.removePendingGroup(id);
    },

    clickRemove: function(){
        var id = this.props.groupID;
        this.props.removePendingGroup(id);
    },

    render: function(){
      var li_key = this.props.groupID + "." + "li";
      var span_key = this.props.groupID + "." + "span";
      var i_key = this.props.groupID + "." + "i";
      var i_key2 = this.props.groupID + "." + "i2";
      var a_key = this.props.groupID + "." + "a";
      var ul_key = this.props.groupID + "." + "ul";
        return(
            <li className="pendingGroupDiv mdl-list__item" key={li_key}>
                <span className="groupListItem mdl-list__item-primary-content" key={span_key}>
                    <i className="groupListItem material-icons" key={i_key}>group</i>
                    {this.props.groupID}
                </span>
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onClick={this.clickSub}>
                Subscribe
                </button>
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onClick={this.clickRemove}>
                Remove
                </button>
            </li>
        )
    }
});
