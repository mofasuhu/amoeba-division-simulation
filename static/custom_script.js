document.addEventListener('DOMContentLoaded', function() {
    const legendHtml = `
        <style>
            #legend {
                margin-top: 20px;
            }

            #legend ul {
                list-style-type: none;
            }

            #legend li {
                margin: 5px;
                padding: 5px;
            }

            #legend span {
                padding: 2px 5px;
                margin-right: 10px;
                border: 1px solid #000;
            }
        </style>
        <div id="legend" style="position: absolute; top: 100px; left: 50px; width: 200px;">
            <h3>Legend</h3>
            <ul>
                <li><span style="background-color: green; width: 20px; display: inline-block;">&nbsp;</span> Intact</li>
                <li><span style="background-color: blue; width: 20px; display: inline-block;">&nbsp;</span> Encysted</li>
                <li><span style="background-color: lightblue; width: 20px; display: inline-block;">&nbsp;</span> Excysted</li>
                <li><span style="background-color: red; width: 20px; display: inline-block;">&nbsp;</span> Divided</li>
                <li><span style="background-color: orange; width: 20px; display: inline-block;">&nbsp;</span> Stressed</li>
                <li><span style="background-color: yellow; width: 20px; display: inline-block;">&nbsp;</span> Dividing</li>
            </ul>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', legendHtml);
});
