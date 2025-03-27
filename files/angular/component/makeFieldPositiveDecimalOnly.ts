makeFIELD_NAMEPositiveDecimalOnly() {
    var str = this.TABLE_NAME.FIELD_NAME!.toString();
    var first = str.substring(0, 1);
    var first_is_num;
    var second_is_num;
    var decimal_location;
    var the_rest_is_num;
    var the_rest_is_num_2;
    var secondletter;
    var answer;
    var last = str.substring(str.length-1);
    var lengthBeforeDigits = this.FIELD_NAMEMax - this.FIELD_NAMESigDigits;
    if(str.length==1) {
      // first number must be a number, not a period
      first_is_num = /[0-9]/.test(first);
      answer = first_is_num;
    } else {
      if(str.length==2) {
        //console.log("testing 2-digit number");
        first_is_num = /[0-9]/.test(first);
        secondletter = str.substring(1,2);
        second_is_num = /[0-9]/.test(secondletter);
        decimal_location = /[.]/.test(secondletter);
        if(decimal_location && lengthBeforeDigits==1) {
          answer = false;
        } else {
          answer = first_is_num && (decimal_location || second_is_num);
        }
      } else if(last == ".") {
        // if this is the only ".", then indexOf(".") == length-1
        if(str.indexOf(".") == str.length-1) {
          //console.log("testing number ending in .");
          answer == true;
        } else {
          answer = false;
        }
      } else {
        // first let's just check in general if this is a decimal #
        first_is_num = /[0-9]/.test(first);
        //console.log("first number is " + firstgood);
        the_rest_is_num = /^[0-9.]\d*(\.\d+)?$/.test(str.substring(1));
        the_rest_is_num_2 = /^\d*(\.\d+)?$/.test(str.substring(1));
        //console.log("isnum = : " + isnum);
        answer = first_is_num && the_rest_is_num_2;
        if(answer == true) {
          // now we need to verify that the chunks before and after the "." period
          // are within the number's range
          decimal_location = str.indexOf(".");
          if(decimal_location == -1) {
            // whole number still
            if(str.length>lengthBeforeDigits) {
              answer = false;
            }
          } else {
            var tempstr = str.substring(str.indexOf(".")+1);
            if(tempstr.length>this.FIELD_NAMESigDigits) {
              answer = false;
            }
          }
        }
      }
    }
    if(answer == false) {
      str = str.substring(0,str.length-1);
      last = str.substring(str.length-1);
      if(last == ".") {
        do {
          str = str.substring(0,str.length-1);
          last = str.substring(str.length-1);
        } while(last == ".")
      }
      if(str.length==0 || isNaN(this.TABLE_NAME.FIELD_NAME!)) {
        this.TABLE_NAME.FIELD_NAME = null;
      } else {
        this.TABLE_NAME.FIELD_NAME = parseFloat(str);
      }
    }
  }
