import { Component, OnInit } from '@angular/core';

import { ResponseMessage } from '../../models/ResponseMessage';
XXX

@Component({
  selector: 'app-&',
  templateUrl: './&.component.html',
  styleUrls: ['./&.component.css']
})
export class %Component implements OnInit {
  ZZZ
    p: number = 1;
    showExtended: boolean = true;
    loaded: boolean = false;
    alwaysHidden: boolean = true;
    enableAdd: boolean = false;
    show%Form: boolean = false;
    editMode: boolean = false;
    addbarmsg: string = 'Add %';
    formmsg: string = 'Add %';

  YYY

  ngOnInit() {
    this.reload();
  }

  add%() {
    VVV
  }

  onSubmit(e) {
    console.log(123);
    e.preventDefault();
  }

  reload() {
    this.loaded = false;
    WWW
    this.show%Form = false;
    this.editMode = false;
    this.addbarmsg = 'Add %';
    this.formmsg = 'Add %';
  }

  editItem(i: number) {
    this.editMode = true;
    this.addbarmsg = 'Save changes';
    this.formmsg = 'Edit %';
    QQQ
  }

  deleteItem(i: number) {
    SSS
  }
}