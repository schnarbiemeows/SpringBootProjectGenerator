import { Component, OnInit } from '@angular/core';

import { ResponseMessage } from '../../models/ResponseMessage';
IMPORTS

@Component({
  selector: 'app-&',
  templateUrl: './&.component.html',
  styleUrls: ['./&.component.css']
})
export class %Component implements OnInit {
  LIST_ITEM_DTO
  FK_DTO_LISTS
    p: number = 1;
    itemsPerPage: number = 10;
    showExtended: boolean = true;
    loaded: boolean = false;
    alwaysHidden: boolean = true;
    enableAdd: boolean = false;
    show%Form: boolean = false;
    addMode: boolean = false;
    editMode: boolean = false;
    addbarmsg: string = 'Add Field';
    saveChangesMsg: string = 'Save Changes';
    cancelMsg: string = 'Cancel';
    formmsg: string = 'Add %';
    paginationDisabled: boolean = false;
    MINS_&_MAXS

  CONSTRUCTOR

  ngOnInit() {
    this.reload();
    INIT_FK_LISTS
  }

  initiateAdd() {
    //console.log("initiating item add ....")
    this.editMode = false;
    this.addMode = true;
    this.show%Form = true;
    this.paginationDisabled = true;
    CLEAR_ITEM_DTO
  }

  saveResults() {
    CREATE_SERVICE
    this.paginationDisabled = false;
  }

  onSubmit(e) {
    console.log(123);
    e.preventDefault();
  }

  reload() {
    this.loaded = false;
    GET_ALL_RECORDS
    this.show%Form = false;
    this.editMode = false;
    this.addMode = false;
    this.paginationDisabled = false;
  }

  editItem(i: number) {
    this.editMode = true;
    this.paginationDisabled = true;
    this.formmsg = 'Edit %';
    EDIT_SERVICE
  }

  deleteItem(i: number) {
    DELETE_SERVICE
    this.paginationDisabled = false;
  }

  FOREIGN_KEY_CALLS

  VALIDATOR_CALLS
}