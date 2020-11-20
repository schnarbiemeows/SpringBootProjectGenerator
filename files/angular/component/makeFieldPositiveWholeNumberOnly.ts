makeFIELD_NAMEPositiveWholeNumberOnly() {
	var str = this.TABLE_NAME.FIELD_NAME.toString();
	var last = str.substring(str.length-1);
	last_is_num = /[0-9]/.test(last);
	var answer = last_is_num;
	if(answer == false) {
	  str = str.substring(0,str.length-1);
	  if(str.length==0 || isNaN(this.TABLE_NAME.FIELD_NAME)) {
		this.TABLE_NAME.FIELD_NAME = null;
	  } else {
		this.TABLE_NAME.FIELD_NAME = parseInt(str);
	  }
	}
}