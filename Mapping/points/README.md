# Intersection points

Each file stores the ray–OSM intersections for one city, produced by
spatially joining the rays (generated in `ray/`) with the ground-truth
OSM road network.

| Column | Meaning |
|---|---|
| `FID_ray`, `x`, `y` | ray ID and its origin point (detection side) |
| `FID_OSM`, `lx`, `ly` | matched OSM segment and the intersection point |

- `intersect_zhuhai.txt` — Zhuhai, 98,451 rows (10,112 rays × 652 OSM segments)

See `scripts/intersect_rays_osm.py` for a license-free reproduction
(no ArcGIS required).
