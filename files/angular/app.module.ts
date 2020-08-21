import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/Forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgxPaginationModule } from 'ngx-pagination';
import { NavbarComponent } from './components/navbar/navbar.component';
IMPORTS


@NgModule({
  declarations: [
    ADD_DECLARATIONS
  ],
  imports: [
    ADD_MODULES
  ],
  providers: [ADD_PROVIDERS],
  bootstrap: [AppComponent]
})
export class AppModule { }