import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

IMPORTS

const routes: Routes = [
ROUTES
];
;
@NgModule({
  exports: [RouterModule],
  imports: [
    RouterModule.forRoot(routes)
  ],
  providers: []
})
export class AppRoutingModule { }