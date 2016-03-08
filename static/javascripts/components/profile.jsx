var ProfilePage = React.createClass({
getInitialState: function(){
    var departments = '';
    var courses = '';
    var courses_taught = '';
    var status = '';
    
    
    if(user_data[0].departments.length == 0 || user_data[0].departments == ['']){
        departments = 'Not enrolled into any departments';
    }
    else{
        for(var i = 0; i < user_data[0].departments.length; i++){
            departments += user_data[0].departments[i];
            if(i < user_data[0].departments.length-1){
                departments += "\n";
            }
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
                    courses += "\n";
                }
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
    var style = {
        listStyleType: "none",
        fontSize: "20px"
    };

        return(
        <ul style={style}>
            <li>Username: {user_data[0].username}</li>
            <li>Email: {user_data[0].email}</li>
            <li>Birth Date: {user_data[0].dob}</li>
            <li>Gender: {user_data[0].gender}</li>
            <li>Ethnicity: {user_data[0].ethnicity}</li>
            <li>Native Language: {user_data[0].native_language}</li>
            <li>Year: {this.state.status}</li>
        </ul>
    );
    }
});
