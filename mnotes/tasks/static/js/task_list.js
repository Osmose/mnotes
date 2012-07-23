(function(ko, $) {
    function Task(data) {
        this.id = ko.observable(data.id);
        this.title = ko.observable(data.title || '');
        this.is_done = ko.observable(data.is_done || false);
        this._delete = ko.observable(false);
        this.updated = ko.observable(new Date());
    }

    function TaskListViewModel() {
        var self = this;
        self._tasks = ko.observableArray([]);
        self.tasks = ko.computed(function() {
            return self._tasks().filter(function(task) {
                return task._delete() === false;
            });
        });

        self.task_title = ko.observable();

        self.addTask = function() {
            self._tasks.push(new Task({title: self.task_title()}));
            self.task_title('');
        };

        self.removeTask = function(task) {
            task._delete(true);
        };

        self.user_id = ko.observable(null);
        self.user_email = ko.observable('');
        self.user_key = ko.observable('');
        self.login = function() {
            navigator.id.get(function(assertion) {
                $.ajax('login', {
                    data: {
                        assertion: assertion
                    },
                    type: 'post'
                }).done(function(data) {
                    var user = data.user;
                    self.user_id(user.id);
                    self.user_email(user.email);
                    self.user_key(user.key);
                    self.sync();
                }).fail(function() {
                    self.user_id(null);
                    self.user_email('');
                    self.user_key('');
                    throw 'Login failed!';
                });
            });
        };
        self.logout = function() {
            $.ajax('logout', {
                type: 'post'
            }).done(function() {
                self.user_id(null);
                self.user_email('');
                self.user_key('');
                self._tasks.removeAll();
            });
        };

        self.bookmarklet_code = ko.computed(function() {
            return ("javascript: (function () { " +
                "var jsCode = document.createElement('script'); " +
                "jsCode.setAttribute('src', " +
                    "'http://localhost:8000/static/js/bookmarklet.js'); " +
                "document.body.appendChild(jsCode); mnotes.addTask('" +
                self.user_key() + "'); }());");
        });

        $.ajax('user').done(function(data) {
            var user = data.user;
            self.user_id(user.id);
            self.user_email(user.email);
            self.user_key(user.key);
            self.sync();
        });

        self.is_syncing = ko.observable(false);
        self.sync = function() {
            self.is_syncing(true);
            $.ajax('tasks', {
                data: {tasks: ko.toJSON(self._tasks)},
                type: 'post'
            }).done(function(data) {
                self._tasks([]);
                data.tasks.forEach(function(t) {
                    self._tasks.push(new Task(t));
                });
                self.is_syncing(false);
                console.log('Tasks synced successfully!');
            }).fail(function() {
                self.is_syncing(false);
                throw 'Error syncing tasks!';
            });
        };
    }

    ko.applyBindings(new TaskListViewModel());
})(ko, jQuery);