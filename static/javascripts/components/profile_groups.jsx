var ProfileGroups = React.createClass({
    getInitialState: function(){
        return({
            currentGroups: [],
            pendingGroups: [],
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
        
    refreshData: function(){
        $.ajax({
                url: this.props.routes.groups,
                type: 'GET',
                dataType: "json",
                success: function(data){
                    var currentGroups = this.state.currentGroups
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
    
    componentDidMount: function(){
        $.ajax({
                url: this.props.routes.groups,
                type: 'GET',
                dataType: "json",
                success: function(data){
                    var currentGroups = this.state.currentGroups
                    currentGroups = data
                    this.setState({
                        currentGroups: data,
                    })
                }.bind(this),
                error: function(xhr, status,err){
                    console.log('error');
                }.bind(this)
        });
    },
    
    render: function(){
    
      var renderedGroups = this.state.currentGroups.map((group,i) => {
      if(this.state.currentGroups.length > 0){
        return (
        <GroupDiv key={group.id} unsubscribeGroup={this.unsubscribeGroup} groupID = {group}/>
        )
      }
      else{
          return (
          <div key={group.id}></div>
        )
      }
      });
      
      return(    
          <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
              <div className="mdl-card__title mdl-card--expand mdl-color--primary">
                <h2 className="mdl-card__title-text"> My Groups </h2>
              </div>  
              <div className="mdl-cell mdl-cell--12-col">
                <ul className= "mdl-list">
                    {renderedGroups}
                </ul>
              </div>
            <div className="mdl-card__title mdl-card--expand mdl-color--primary">
              <h2 className="mdl-card__title-text"> Subscribe to a Group </h2>
            </div>  
            <SubscribeDiv refreshData={this.refreshData} routes={this.props.routes}/>
          </div>
      );
    }
});

var GroupDiv = React.createClass({

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
            <li className="mdl-list__item" key={li_key}>
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

var SubscribeDiv = React.createClass({
    
    getInitialState: function(){
        return{
            group: ''
        }
    },
    
    handleChange: function(e){
        this.setState({group: e.target.value});
    },
    
    subscribe: function(){
        var subJSON = {
            "id": this.state.group,
            "action": "sub"
        }
        console.log(subJSON);
        $.ajax({
            url: this.props.routes.subscribe,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(subJSON),
            success: function(data){
                this.props.refreshData();
            }.bind(this),
            error: function(xhr, status,err){
                console.log('error');
            }.bind(this)
        });    
    },
    
    render: function(){
        return(
        <span>
          <div className="mdl-textfield mdl-js-textfield mdl-cell mdl-cell--8-col">
              <input className="mdl-textfield__input"
              type="text" 
              value={this.state.group} 
              onChange={this.handleChange}/>
              <label className="mdl-textfield__label">GroupID here...</label>
          </div>
          <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.subscribe}>
                Subscribe
          </button>
        </span>
        );
    }
});