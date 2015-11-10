var Table = React.createClass({
   render: function(){
      return(
        <table className= "mdl-js-data-table mdl-data-table--selectable">
            <thead>
              <tr>
                <th className="mdl-data-table__cell--non-numeric">Material</th>
                <th>Quantity</th>
                <th>Unit price</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="mdl-data-table__cell--non-numeric">Acrylic (Transparent)</td>
                <td>250</td>
                <td>$2.90</td>
              </tr>
              <tr>
                <td className="mdl-data-table__cell--non-numeric">Plywood (Birch)</td>
                <td>50</td>
                <td>$1.25</td>
              </tr>
              <tr>
                <td className="mdl-data-table__cell--non-numeric">Laminate (Gold on Blue)</td>
                <td>10</td>
                <td>$12.35</td>
              </tr>
            </tbody>
        </table>
      );
   }
});
