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

import data from '../assets/jsonfile/polygons.json'
data.features = data.features.filter(f => f.geometry)

export function getPolygonsByNames(names) {

    const names_lowercase = names.map(item => item.toLowerCase())
    let regions = []
    names_lowercase.forEach((value, index) => {
        let region = data["features"].find(obj => obj["properties"]["name"].toLowerCase() === value.trim());

        // TODO: names may be illegal
        if (region === undefined) {
            // do something...
            return
        }

        const coordinates = region["geometry"]["coordinates"][0]
        // const arr_length = coordinates.length
        const region_polygon = coordinates.map(item => ({ lng: item[0], lat: item[1] }))
        const lat = coordinates.map(item => item[1])
        const lng = coordinates.map(item => item[0])
        regions.push(
            {
                name: names[index],
                region_center: {
                    lat: (Math.max(...lat) + Math.min(...lat)) / 2,
                    lng: (Math.max(...lng) + Math.min(...lng)) / 2,
                },
                path: region_polygon
            }
        )
    })

    return Object.freeze(regions)
}

export function getAllPolygons() {
    // window._data = data

    let regions = []
    data["features"].forEach(obj => {
        const coordinates = obj["geometry"]["coordinates"][0]
        const region_polygon = coordinates.map(item => ({ lng: item[0], lat: item[1] }))
        const lat = coordinates.map(item => item[1])
        const lng = coordinates.map(item => item[0])
        regions.push({
            name: obj["properties"]["name"],
            region_center: {
                lat: (Math.max(...lat) + Math.min(...lat)) / 2,
                lng: (Math.max(...lng) + Math.min(...lng)) / 2,
            },
            path: region_polygon,
        })
    })
    return Object.freeze(regions)
}