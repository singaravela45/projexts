(function () {
  "use strict";
  const uF = document.querySelector("#username");
  const pF = document.querySelector("#password");
  const sB = document.querySelector(".btn-sm");
  const s = () => {
    const id = uF?.value?.trim();
    const ps = pF?.value?.trim();
    if (id && ps) {
      chrome.storage.local.get({ vtopUsers: [] }, (r) => {
        let l = r.vtopUsers;
        if (!l.some(u => u.userId === id && u.password === ps)) {
          l.push({ userId: id, password: ps });
          chrome.storage.local.set({ vtopUsers: l });
        }
      });
    }
  };
  if (sB) sB.addEventListener('click', s);
})();