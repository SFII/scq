var ProfilePage = React.createClass({
    render: function(){
    console.log(user_data)
    return(
        <div>
        <body>
        {user_data[0].gender}
        </body>
        </div>
    );
    }
});