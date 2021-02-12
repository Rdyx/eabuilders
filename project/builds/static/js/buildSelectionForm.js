document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('select[name^="skill_"]').forEach(element => test(element));
    document.querySelectorAll('select[name^="item_"]').forEach(element => test2(element));
}, false);



function test(e) {
    target_div = document.getElementById(e.name);
    target_img = document.getElementById(e.name+'_img');
    target_name = document.getElementById(e.name+'_name');
    target_desc = document.getElementById(e.name+'_desc');
    target_range = document.getElementById(e.name+'_range');
    target_targets = document.getElementById(e.name+'_targets');
    target_cd = document.getElementById(e.name+'_cd');

    skill = skills.filter(skill => skill.pk.toString() === e.value)[0];
    if (skill) {
        skill_fields = skill.fields;

        if (skill_fields) {
            skill_color = skill_fields.deprecated ? 'black' : skill_fields.stype[1];
            console.log(skill_fields, e.name)
            target_img.style.backgroundImage = "url(/media/"+skill_fields.img+"), radial-gradient("+skill_color+","+skill_color+",black)";

            target_name.innerHTML = skill_fields.name;
            target_name.style.color = skill_color;

            target_desc.innerHTML = skill_fields.desc;
            target_range.innerHTML = skill_fields.range;
            target_targets.innerHTML = skill_fields.targets;
            target_cd.innerHTML = skill_fields.cd;

            target_div.classList.remove('hidden');

            // target_div.innerHTML = skill.fields.desc;
        } else {
            target_div.classList.add('hidden');
        }
    }
}

function test2(e) {
    target_div = document.getElementById(e.name);
    target_img = document.querySelector("#"+e.name+'_img img');
    race_img = document.querySelector("#"+e.name+'_img_race');
    material_img = document.querySelector("#"+e.name+'_img_material');
    console.log(target_img)
    target_name = document.getElementById(e.name+'_name');
    target_desc = document.getElementById(e.name+'_desc');

    buy = document.getElementById(e.name+'_buy');
    sell = document.getElementById(e.name+'_sell');
    hp = document.getElementById(e.name+'_hp');
    phys_atk = document.getElementById(e.name+'_phys_atk');
    mag_atk = document.getElementById(e.name+'_mag_atk');
    pyhs_def = document.getElementById(e.name+'_pyhs_def');
    mag_def = document.getElementById(e.name+'_mag_def');
    acc = document.getElementById(e.name+'_acc');
    res = document.getElementById(e.name+'_res');
    ign_phys = document.getElementById(e.name+'_ign_phys');
    ign_mag = document.getElementById(e.name+'_ign_mag');
    speed = document.getElementById(e.name+'_speed');
    crit_rate = document.getElementById(e.name+'_crit_rate');
    crit_dmg = document.getElementById(e.name+'_crit_dmg');

    // target_range = document.getElementById(e.name+'_range');
    // target_targets = document.getElementById(e.name+'_targets');
    // target_cd = document.getElementById(e.name+'_cd');

    skill = items.filter(skill => skill.pk.toString() === e.value)[0];
    if (skill) {
        console.log(skill)
        skill_fields = skill.fields;

        if (skill_fields) {
            skill_color = "text-" + tiers_colors[skill_fields.tier];
            console.log(skill_color)
            console.log(skill_fields, e.name)
            // target_img.style.backgroundImage = "url(/media/"+skill_fields.img+")"; //, radial-gradient("+skill_color+","+skill_color+",black)";
            target_img.src = "/media/"+skill_fields.img; //, radial-gradient("+skill_color+","+skill_color+",black)";
            race_img.src = "/media/"+skill_fields.race[0]; //, radial-gradient("+skill_color+","+skill_color+",black)";
            material_img.src = "/media/"+skill_fields.material[0]; //, radial-gradient("+skill_color+","+skill_color+",black)";

            target_name.innerHTML = skill_fields.name;
            target_name.classList.add(skill_color);

            target_desc.innerHTML = skill_fields.desc;

            buy.innerHTML = skill_fields.buy_cost
            sell.innerHTML = skill_fields.sell_cost

            hp.innerHTML = skill_fields.hp
            phys_atk.innerHTML = skill_fields.hp
            mag_atk.innerHTML = skill_fields.hp
            pyhs_def.innerHTML = skill_fields.hp
            mag_def.innerHTML = skill_fields.hp
            acc.innerHTML = skill_fields.hp
            res.innerHTML = skill_fields.hp
            ign_phys.innerHTML = skill_fields.hp
            ign_mag.innerHTML = skill_fields.hp
            speed.innerHTML = skill_fields.hp
            crit_rate.innerHTML = skill_fields.hp
            crit_dmg.innerHTML = skill_fields.hp
            // target_range.innerHTML = skill_fields.range;
            // target_targets.innerHTML = skill_fields.targets;
            // target_cd.innerHTML = skill_fields.cd;

            target_div.classList.remove('hidden');

            // target_div.innerHTML = skill.fields.desc;
        } else {
            target_div.classList.add('hidden');
        }
    }
}