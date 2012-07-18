$.vifib.login = {
    facebook: function (params) {
        var redirect = window.location.origin + window.location.pathname + '#/dashboard/' + '?',
        fburl = 'https://www.facebook.com/dialog/oauth?' +
            'client_id=' + $(document).slapos('store', 'fbappid') +
            '&redirect_uri=' + encodeURIComponent(redirect) +
            '&scope=email' +
            '&response_type=token';
        // set token type to Facebook for js library
        $(document).slapos('store', 'token_type', 'Facebook');
        window.location.href = fburl;
    },
    google: function (params) {
        var redirect = window.location.origin + window.location.pathname + '?',
            ggurl = 'https://accounts.google.com/o/oauth2/auth?' +
                'client_id=' + $(document).slapos('store', 'ggappid') +
                '&redirect_uri=' + encodeURIComponent(redirect) +
                '&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email++https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile' +
                '&response_type=token';
        $(document).slapos('store', 'token_type', 'Google');
        window.location.href = ggurl;
    }
}
$.vifib.statuscode = {
    400: function (jqxhr, textstatus) {
        $.vifib.replacepanel($(this), $.vifib.panel.badrequest);
    },
    401: function (jqxhr, textstatus) {
        $.url.redirect('/login');
    },
    402: function (jqxhr, textstatus) {
        $.vifib.replacepanel($(this), $.vifib.panel.payment);
    },
    404: function (jqxhr, textstatus) {
        $.vifib.replacepanel($(this), $.vifib.panel.notfound);
    },
    500: function (jqxhr, textstatus) {
        $.vifib.replacepanel($(this), $.vifib.panel.internalerror);
    },
}
$.vifib.softwareList = function (context) {
    var list;
    return context.each(function () {
        list = $(this).find('ul');
        $(this).slapos('softwareList', {
            success: function (response) {
                $.each(response.list, function (index, soft) {
                    var row = $.vifib.fillRowSoftware($('<li></li>'), soft);
                    list.append(row);
                });
                list.listview('refresh');
            }
        });
    });
}

$.vifib.instanceList = function (context) {
    var list;
    return context.each(function () {
        list = $(this).find('ul');
        $(this).slapos('instanceList', {
            success: function (response) {
                $.when(
                    $.vifib.fillRowInstance(list, $('<li></li>'), response.list[0])
                ).then(function () {
                    list.listview('refresh');
                });
                //$.when.apply($(this), $.map(response.list, function (inst) {
                    //$.vifib.fillRowInstance(list, $('<li></li>'), inst);
                //})).done(function (a, b, c) {
                    //console.log(arguments);
                    //list.listview('refresh');
                //});
            },
        });
    });
}
$.vifib.fillRowInstance = function (list, row, instid) {
    return row.slapos('instanceInfo', instid, {
        success: function (response) {
            $.extend(response, {insturl: '#/dashboard/instance/id' + instid});
            $(this).html(Mustache.render($.vifib.panel.rowinstance, response));
        },
        complete: function (jqxhr, textstatus) {
            list.append($(this));
        }
    });
}
$.vifib.computerList = function (context) {
    var list;
    return context.each(function () {
        list = $(this).find('ul');
        $(this).slapos('computerList', {
            success: function (response) {
                $.each(response.list, function (index, comp) {
                    var row = $.vifib.fillRowComputer($('<li></li>'), comp);
                    list.append(row);
                });
                list.listview('refresh');
            }
        });
    });
}
$.vifib.fillRowSoftware = function (context, softid) {
    return context.each(function () {
        $(this).slapos('softwareInfo', softid, {
            success: function (response) {
                $.extend(response, {softurl: '#/library/software/id' + softid});
                $(this).html(Mustache.render($.vifib.panel.rowsoftware, response));
            }
        });
    })
}
$.vifib.fillRowComputer = function (context, compid) {
    return context.each(function () {
        $(this).slapos('computerInfo', compid, {
            success: function (response) {
                $.extend(response, {compurl: '#/dashboard/computer/id/' + compid});
                $(this).html(Mustache.render($.vifib.panel.rowcomputer, response));
            }
        });
    })
}