const addPadding = (selector, styleName, styleValue) => {
  let el = document.querySelector(selector);
  el.style[styleName] = styleValue;
};
addPadding(
  replace_str_selector,
  replace_str_style_name,
  replace_str_style_value
);
return "finished";
