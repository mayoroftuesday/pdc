/*
Hide all submenus
*/
function hideMenus() {
  var menuitems = document.querySelectorAll("ul.primary > li");
  for (var i = 0; i < menuitems.length; i++) {
    var menuitem = menuitems[i];

    // hide submenu
    menuitem.classList.remove("focused");
    var anchor = menuitem.querySelector("a");
    if (anchor.hasAttribute("aria-expanded")) {
      anchor.setAttribute("aria-expanded", "false");
    }
  }
}

/*
Show submenu under a top level menu item
*/
function showMenu(menuitem) {
  // first, hide all menus
  hideMenus();

  // then display the submenu
  menuitem.classList.add("focused");
  var anchor = menuitem.querySelector("a");
  if (anchor.hasAttribute("aria-expanded")) {
    anchor.setAttribute("aria-expanded", "true");
  }

  // adjust submenu if it goes outside right window border
  var submenu = menuitem.querySelector("ul");
  if (submenu) {
    var rightBound = document.body.getBoundingClientRect().right;
    var submenuRightBound = submenu.getBoundingClientRect().right;
    if (submenuRightBound > rightBound) {
      submenu.style.right = "10px";
    }
  }
}

/*
Handle opening menus
*/
function menuOnHandler(evt) {
  // prevent navigation to placeholder "#"
  if (evt.target.href.endsWith("#")) {
    evt.preventDefault();
  }

  // show the submenu
  var topMenuElement = evt.target.closest("ul.primary > li");
  showMenu(topMenuElement);
}

/*
Keyboard handler for opening and closing menus
*/
function menuKeyboardOnHandler(evt) {
  if (evt.code === "Enter") {
    // Use enter to click link and expand submenu
    menuOnHandler(evt);
  } else if (evt.code === "Escape") {
    // Use escape to close menus
    hideMenus();
  }
}

/*
Handle closing of menus
*/
function menuOffHandler(evt) {
  var topMenuElement = evt.target.closest("ul.primary > li");
  var currentElement = document.elementFromPoint(evt.clientX, evt.clientY);

  // only hide menu if the user has moved on to an element not
  // within the menu
  if (!topMenuElement || !topMenuElement.contains(currentElement)) {
    hideMenus();
  }
}

function menuSetup() {
  var submenus = document.querySelectorAll("ul.primary > li");
  for (var i = 0; i < submenus.length; i++) {
    var submenu = submenus[i];

    // mouse hover events
    submenu.addEventListener('mouseover', menuOnHandler);
    submenu.addEventListener('mouseout', menuOffHandler);

    // mouse click or mobile touch
    submenu.addEventListener('mousedown', menuOnHandler);

    // keyboard
    submenu.addEventListener('keydown', menuKeyboardOnHandler);
  }

  // mouse click or mobile touch outside of menu
  document.addEventListener('mousedown', menuOffHandler);
}
