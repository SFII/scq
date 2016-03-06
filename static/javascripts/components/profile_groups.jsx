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
                console.log('success');
            }.bind(this),
            error: function(xhr, status,err){
                console.log('error');
            }.bind(this)
        });   
        
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
      const renderedGroups = this.state.currentGroups.map((group,i) => {
      var li_key = group + "." + "li";
      var span_key = group + "." + "span";
      var i_key = group + "." + "i";
      var i_key2 = group + "." + "i2";
      var a_key = group + "." + "a";
      var div_key = group + "." + "div";
      var ul_key = group + "." + "ul";
      if(this.state.currentGroups.length > 0){
        return (
            <li className="mdl-list__item" key={li_key}>
                <span className="mdl-list__item-primary-content" key={span_key}>
                <i className="material-icons  mdl-list__item-avatar" key={i_key}>group</i>
                    {group}
                </span>
                <a className="mdl-list__item-secondary-action" key={a_key}><i className="material-icons" key = {i_key2} onClick={this.unsubscribeGroup.bind(this,group)}>star</i></a>    
            </li>
        )
      }
      else{
          return (
          <div key={div_key}></div>
        )
      }
      });
      return(
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <ul className= "mdl-list">
                {renderedGroups}
            </ul>
          </div>
      );
    }
});