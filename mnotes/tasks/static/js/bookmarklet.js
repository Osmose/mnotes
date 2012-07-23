    window.mnotes = {
        addTask: function(key) {
            if (mnotes.isBugzilla()) {
                mnotes.handleBugzilla(key);
            }
        },

        createTask: function(key, title) {
            var jsCode = document.createElement('script');
            jsCode.setAttribute('src',
                                'http://localhost:8000/jsonp/create_task?key=' +
                                encodeURIComponent(key) + '&title=' +
                                encodeURIComponent(title));
            document.body.appendChild(jsCode);
        },

        handleResponse: function(data) {
            if ('error' in data) {
                alert('Error: ' + data.error);
            } else {
                alert('Task added!');
            }
        },

        isBugzilla: function() {
            return document.getElementsByTagName("body")[0].className.indexOf('bz_bug') !== -1;
        },

        handleBugzilla: function(key) {
            var description_elem = document.getElementById('short_desc_nonedit_display');
            var title = description_elem.innerHTML;
            mnotes.createTask(key, title);
        }
    };