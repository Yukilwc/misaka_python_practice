const removeEl = (selector) => {
  let elList = document.querySelectorAll(selector);
  if (elList && elList.length > 0) {
    elList.forEach((el) => el.remove());
  }
};
removeEl(replace_str_selector);
return "remove el finished";
