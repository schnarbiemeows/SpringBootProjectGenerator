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
    p: number = 1;
    showExtended: boolean = true;
    loaded: boolean = false;
    alwaysHidden: boolean = true;
    enableAdd: boolean = false;
    show%Form: boolean = false;
    editMode: boolean = false;
    addbarmsg: string = 'Add %';
    formmsg: string = 'Add %';

  CONSTRUCTOR

  ngOnInit() {
    this.reload();
  }

  add%() {
    CREATE_SERVICE
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
    this.addbarmsg = 'Add %';
    this.formmsg = 'Add %';
  }

  editItem(i: number) {
    this.editMode = true;
    this.addbarmsg = 'Save changes';
    this.formmsg = 'Edit %';
    EDIT_SERVICE
  }

  deleteItem(i: number) {
    DELETE_SERVICE
  }
}