const excel_file = document.getElementById('excel_file');

excel_file.addEventListener('change', (event) => {

    if(!['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'].includes(event.target.files[0].type))
    {
        document.getElementById('excel_data').innerHTML = '<div class="alert alert-danger">Only .xlsx or .xls file format are allowed</div>';

        excel_file.value = '';

        return false;
    }
    var texts = document.querySelectorAll('p');
    /*for(var i = 0; i<texts.length; i++)
            {
                    texts[i].
            }*/

    document.getElementById('footer').style.visibility = 'hidden';

    var reader = new FileReader();

    reader.readAsArrayBuffer(event.target.files[0]);

    reader.onload = function(event) {
        var data = new Uint8Array(reader.result);
        var work_book = XLSX.read(data, {type:'array'});
        var sheet_name = work_book.SheetNames;
        var sheet_data = XLSX.utils.sheet_to_json(work_book.Sheets[sheet_name[0]], {header:1});

        if(sheet_data.length > 0)
        {
            var DoData = new Array(sheet_data.length);
            var PosleData = new Array(sheet_data.length);
            var TempData = new Array(sheet_data.length);
            var RasxData = new Array(sheet_data.length);

            for(var row = 3; row < sheet_data.length; row++)
            {
								//NewData[row-3] = new Array(1);
                for(var cell = 0; cell < sheet_data[row].length; cell++)
                {
                    if(sheet_data[row][cell] != '#N/A' || sheet_data[row][cell] != '0')
                    {
                        switch (cell)
                        {
                            case 1:
                            {
                                DoData[row-3] = sheet_data[row-1][cell];
                                break;
                            }
                            case 2:
                            {
                                PosleData[row-3] = sheet_data[row-1][cell];
                                break;
                            }
                            case 3:
                            {
                                TempData[row-3] = sheet_data[row-1][cell];
                                break;
                            }
                            case 4:
                            {
                                RasxData[row-3] = sheet_data[row-1][cell];
                                break;
                            }
                        }
                    }
                }
            }
        }

        for(var i =0; i<texts.length; i++)
        {
            texts[i].addEventListener('click',
            function(e)
            {
                 switch (e.target.getAttribute('id'))
                     {
                        case 'first_column':
                        {
                            localStorage.setItem("Do", JSON.stringify(DoData));
                            break;
                        }
                        case 'second_column':
                        {
                            localStorage.setItem("Do", JSON.stringify(PosleData));
                            break;
                        }
                        case 'third_column':
                        {
                            localStorage.setItem("Do", JSON.stringify(TempData));
                            break;
                        }
                        case 'fourth_column':
                        {
                            localStorage.setItem("Do", JSON.stringify(RasxData));
                            break;
                        }
                     }
                     window.open('data_graph','','Toolbar=1,Location=0,Directories=0,Status=0,Menubar=0,Scrollbars=0,Resizable=Yes,Width=1200,Height=600, Left = 350, Top = 200, position: relative;');

            })
        }

        /*for(var i = 0; i<texts.length; i++)
        {
                texts[i].style.display = '';
        }*/
        document.getElementById('footer').style.visibility = 'visible';
    }

});
