//
//  ContentView.swift
//  LibraryLens
//
//  Created by Cyril Marceau on 21/11/2024.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            Tab("Films", systemImage: "film") {
                MovieView()
            }


            Tab("Series", systemImage: "tv") {
                Text("Series tab")
            }


            Tab("Livres", systemImage: "book") {
                Text("Livres tab")
            }
        }
        .tabViewStyle(.sidebarAdaptable)
        .tabViewSidebarBottomBar {
            MovieView()
        }
    }
}

#Preview {
    ContentView()
}
