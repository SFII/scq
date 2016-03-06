var ProfilePage = React.createClass({
  getInitialState: function(){
    var user_groups = '';
    var user_status = '';
    var num_sub_groups = user_data[0].subscribed_groups.length;
    if ((num_sub_groups == 0) || (user_data[0].subscribed_groups == [''])) {
      user_groups = 'Not subscribed into any groups';
    } else {
      for (var i = 0; i < num_sub_groups; i++) {
        user_groups += user_data[0].subscribed_groups[i];
        if (i < num_sub_groups - 1) {
          user_groups += "\n";
        }
      }
    }
    if (user_data[0].primary_affiliation == "Student") {
      if (user_data[0].status) {
        user_status = user_data[0].status;
      } else {
        user_status = "Did not specify academic year";
      }
    }
    return {
      username: user_data[0].username,
      user_affiliation: user_data[0].primary_affiliation,
      email: user_data[0].email,
      user_gender: user_data[0].gender,
      user_ethnicity: user_data[0].ethnicity,
      user_native_language: user_data[0].native_language,
      user_status: user_data[0].status,
      user_groups: user_groups,
      affiliation: extra_data[0].primary_affiliation,
      gender: extra_data[0].gender,
      ethnicity: extra_data[0].ethnicity,
      native_language: extra_data[0].native_language,
      status: extra_data[0].status,

    };
  },
  _onClick: function() {
    var message = "hello world";
    this.setState({message});
  },
  handleChange: function(key) {
    return function (e) {
      var state = {};
      state[key] = e.target.value;
      this.setState(state);
    }.bind(this);
  },
  render: function(){
    var style = {
      listStyleType: "none",
      fontSize: "20px"
    };
    return(
      <ul style={style}>
      Username: <input value={this.state.username} onChange={this.handleChange('username')} /><br/>
      Affiliation(s): <select>
                        <option value={this.state.user_affiliation}>{this.state.user_affiliation}</option>
                        <option value={this.state.affiliation}>{this.state.affiliation}</option>
                      </select><br/>
      Email: <input value={this.state.email} onChange={this.handleChange('email')} /><br/>
      Birth Date: <input type="text" value={user_data[0].dob}/><br/>
      Gender: <select>
                <option value={this.state.user_gender}>{this.state.user_gender}</option>
                <option value={this.state.gender}>{this.state.gender}</option>
              </select><br/>
      Ethnicity: <select>
                   <option value={this.state.user_ethnicity}>{this.state.user_ethnicity}</option>
                   <option value={this.state.ethnicity}>{this.state.ethnicity}</option>
                 </select><br/>
      Native Language: <select>
                         <option value={this.state.user_native_language}>{this.state.user_native_language}</option>
                         <option value={this.state.native_language}>{this.state.native_language}</option>
                       </select><br/>
      Academic Year: <select>
                       <option value={this.state.user_status}>{this.state.user_status}</option>
                       <option value={this.state.status}>{this.state.status}</option>
                     </select><br/>
      Group(s) Subscribed: <textarea name="courses" cols="30" rows="5" value={this.state.user_groups} /><br/>
      <br/>
      <button onClick={this._onClick} value="Change Message">{this.state.message}</button>
      </ul>
      );
    }
});
