### backend django final HW, kickstartcoding
### June 29, 2021
#### joachim byrnes-shay
#### complete dashboard app,  GITHUB REPOSITORY STATISTICS with Pygal charts and custom tables

#### heroku url: http://dashboard-project2.herokuapp.com/

#### github url:  https://github.com/JoachimByrnesShay/dashboard_project2


github repository statistics


FEATURES:

several fake users and panel/collection data already populate the database.   registration is open.

2 ORM models, many-to-many relationship between PanelsCollection and Panel

caching is utilized per template fragment only for tables (which are not pygal tables) on pages which are heavy on displaying table data

pygal chart svgs have been stored as text data in the database, and so all other chart types other than table do not cost any API calls

login/signup with user-facing dashboard implementing CRUD for Panels and for PanelsCollections.   additionally, users can edit their own account data: name, bio, email, password

several custom template tags have been added in github_dashboards/template_tags, including for dynamically sizing font-size of tables based upon panel size

TypeChoices has been utilized in github_dashboards/models

github_dashboard/models is not a single file but a folder named 'models' where 2 contained files split the 2 models, and a 3rd file exists for a mixin class which contains the primary custom instance methods for Panel (this file is imported in Panel.py and the class is mixed-in to the Panel model)

Tables and pygal charts utilize the same model, and much of the difference is controlled by hiding/disabling/unrequiring or showing/enabling/requiring form fields upon listen to the panel_type form field, along with appropriate validators.  custom javascript is utilized to assist in this regard and is found in static/javascript.  Additional care with this javascript script was taken to ensure that if there is a validation error upon selecting 'table of repos', the form continues to conceal the undesired fields, until the user specifically changes to a different table option (or navigages away from the page and returns to face the default)

upon new form or edit form of panels or collections python scripting is used to validate on whether github-username actually exists, and in case of non-table panels, if repo name actually exists at the point of form entry.   Form will not validate if not.

python scripting is used at point of registration form and also logged-in user account edit form, to check email.  scripting will not allow to validate if the email domain the user attempts to register with or attempts to change their existing email to does not actuall exist.  I recognize in real-use case email verification by email send (send user email to verify) would be a solid method, but in this case, the aim was for a demonstrable app where users can easily populate user accounts without having to complete such a process.   That is,  fake emails such as THISISFAKE@gmail.com and IAMNOTREAL@yahoo.com work with this app.   JimSmith@yahoo.gmail.net.com or david@nowayisthisreal.qrst, for example, will not pass validation.  This is above and beyond Django's own ready-to-go validators and is more precise and encompassing than can be accomplished with regular expressions.  

additional pages are built into the app including asingle page view of each panel or collection; view all registered users on one page; each user panel links to a dedicated public page for that user with some public data that can be viewed by amyone (anonymous or logged in); logged-in user account page, where authorized user can edit account info and update password;

edit and delete buttons on all panels on panels page; edit and delete buttons on all collections on collections page; All delete buttons trigger a modal with confirmation to delete or cancel option

clicking edit button on panels or collections pages populates form on left side of screen with edited model instance’s data.
“clear” button on top of the form on panels or collections pages to clear form fields.

return to previous page (red button) on several pages employing http referer, with contingency built-in in case the referer is lost by user clearing cache or refreshing same page

6 chart types from pygal are included, in addition to the table option (not a pygal table)
12 colorful styles are included from pygal styles in addition to the defaultstyle 
color styles are not utilized for the custom table option, which is html table and not a pygal chart.

in the user app (user/forms.py),
helper text has been custom defined, including for username and and email

usernames have been rendered case-insensitive in this app  to reflect a more typical real-life usage (BILL == bill).  For purposes of this app, emails also must be unique per user account and uniqueness also takes into account case-insensitivyt (BILL@gmail == bill@gmail).   Helper text reflects this, as well as that email domain must exist.

Some work has been done in github_dashboards/admin.py.   PanelsCollectionAdmin class in admin.py uses ‘string_of_panels” method defined for the PanelsCollection class in models to represent <br> separated group of username/reponame being used for the panelcollection, using some truncation of the string data to simplify the presentation, which is conditional per the user passing a falsey argument or not (Default is true == truncate).  While this is used for superficial reference displays elsewhere in the app, it was conceived for usage in admin panel, to give an at glance view on a collection line of what panels compose that collection.