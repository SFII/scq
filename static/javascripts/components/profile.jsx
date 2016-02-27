var ProfilePage = React.createClass({
getInitialState: function(){
    var departments = '';
    var courses = '';
    var courses_taught = '';
    var status = '';
    
    
    if(user_data[0].departments.length == 0 || user_data[0].departments == ['']){
        console.log('default');
        departments = 'Not enrolled into any departments';
    }
    else{
        for(var i = 0; i < user_data[0].departments.length; i++){
            departments += user_data[0].departments[i];
            if(i < user_data[0].departments.length-1){
                console.log("new line");
                departments += "\n";
            }
            console.log("Departments state: " + departments);
        }
    }
    
    if(user_data[0].primary_affiliation == "Student"){
        if(user_data[0].status){
            status = user_data[0].status;
        }
        else{
            status = "Did not specify academic year";
        }
        if(user_data[0].courses.length == 0 || user_data[0].courses == ['']){
            courses = 'Not enrolled into any courses';
        }
        else{
            for(var i = 0; i < user_data[0].courses.length; i++){
                courses += user_data[0].courses[i];
                if(i < user_data[0].courses.length-1){
                    console.log("new line");
                    courses += "\n";
                }
                console.log("Courses state: " + courses);
            }
        }
    }
    
    else if(user_data[0].primary_affiliation[0] == "Faculty"){
        if(user_data[0].courses_taught.length == 0 || user_data[0].courses_taught == ['']){
            courses_taught = 'Not enrolled into any departments';
        }
        else{
            for(var i = 0; i < user_data[0].courses_taught.length; i++){
                courses_taught += user_data[0].courses_taught[i];
                if(i < user_data[0].courses_taught.length-1){
                    courses_taught += "\n";
                }
                console.log("Courses taught state: " + courses_taught);
            }
        }
    }
    return{
    departments: departments,
    courses: courses,
    courses_taught: courses_taught,
    status: status,
    }
},

    render: function(){
    console.log(user_data)
    return(
        <div className="mdl-card mdl-shadow--2dp">
            <div className="mdl-card__title mdl-color--primary">
                <h2 className="mdl-card__title-text">User Info</h2>
            </div>
            <div className="mdl-card__supporting-text">
            Username: {user_data[0].username} <br/>
            User Type: {user_data[0].primary_affiliation} <br/>
            Email: {user_data[0].email} <br/>
            Birth Date: {user_data[0].dob} <br/>
            Gender: {user_data[0].gender} <br/>
            Ethnicity: {user_data[0].ethnicity} <br/>
            Native Language: {user_data[0].native_language} <br/>
            Status: {this.state.status} <br/>
            Courses Enrolled: {this.state.courses} <br/>
            Departments: {this.state.departments} <br/>
            </div>
        </div>
    );
    }
});