/*
{
    type:...
    bbox:...
    crs:...
    features: [
        {
            type: "Feature"
            geometry: {
                type: "MultiPolygon"
                coordinates: []
            },
            properties: {
                prim_pcode: ""
                loc_pid:...
                name: "WEST MELBOURNE"
                state_pid: "2" ----> VIC
            },
            id: ...
        },
        ...
    ]
}

 */

// const fs = require('fs')
// fs.readFile('../assets/jsonfile/polygons.json', 'utf8', function (err, data) {
//     if (err) throw err
//     data = JSON.parse(data)
//     console.log(data["features"][0]["geometry"]["coordinates"][0][0])
//     console.log(data["features"][0]["properties"]["name"])
// })

import * as data from '../assets/jsonfile/polygons.json'

export function getPolygonsByNames(names) {

    const names_lowercase = names.map(item => item.toLowerCase())
    /*
    const regions = []
    names_lowercase.forEach((value, index) => {
        let region = data["features"].find(obj => obj["properties"]["name"].toLowerCase() === value);

        // TODO: names may be illegal
        if (region === undefined) {
            // do something...
            console.log("Region name is not correct")
        }
        else {
            const coordinates = region["geometry"]["coordinates"][0][0]
            const arr_length = coordinates.length
            const region_polygon = coordinates.map(item => new window.google.maps.LatLng(item[0], item[1]))
            regions.push(
                {
                    name: names[index],
                    region_center: {
                        lat: coordinates.reduce((acc, value) => acc + value[0], 0) / arr_length,
                        lng: coordinates.reduce((acc, value) => acc + value[1], 0) / arr_length
                    },
                    path: region_polygon
                }
            )
        }
    })

     */

    return names_lowercase

}

export function getAllPolygons() {

    let regions = []
    data["features"].forEach( obj => {
        const coordinates = obj["geometry"]["coordinates"][0][0]
        console.log(obj["properties"]["name"])
        const arr_length = coordinates.length
        const region_polygon = coordinates.map(item => ({lng: item[0], lat: item[1]}))
        regions.push(Object.freeze({
            name: obj["properties"]["name"],
            region_center: {
                lat: coordinates.reduce((acc, value) => acc + value[1], 0) / arr_length,
                lng: coordinates.reduce((acc, value) => acc + value[0], 0) / arr_length
            },
            path: region_polygon,
        }))
    })
    return Object.freeze(regions)
}