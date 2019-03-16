export default {

  setSessionData: function (key,data) {
    sessionStorage.setItem(key, JSON.stringify(data))
  },
  getSessionData: function (key) {
    var data = sessionStorage.getItem(key);
    if (data != undefined){
      return JSON.parse(data)
    }
    return false
  },
  delSessionData: function (key) {
    sessionStorage.removeItem(key)
  },
  setCurFamily: function (key,data) {
    sessionStorage.setItem(key, data)
  },
  getCurFamily: function (key) {
    return sessionStorage.getItem(key)
  },
  hasValInArrayObj: function (arr, key, val) {
    for (let i = 0; i < arr.length; i++) {
      if (arr[i][key] == val)
        return i;
    }
    return -1;
  }
}
