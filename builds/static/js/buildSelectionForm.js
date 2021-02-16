document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('select[name^="skill_"]').forEach(element => updateSkillDiv(element));
    document.querySelectorAll('select[name^="item_"]').forEach(element => updateItemDiv(element));
}, false);



function updateSkillDiv(e) {
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

            target_img.style.backgroundImage = "url("+media_url+skill_fields.img+"), radial-gradient("+skill_color+","+skill_color+",black)";
            target_name.innerHTML = skill_fields.name;
            target_name.style.color = skill_color;

            target_desc.innerHTML = skill_fields.desc;

            target_range.innerHTML = skill_fields.range;
            target_targets.innerHTML = skill_fields.targets;
            target_cd.innerHTML = skill_fields.cd;

            target_div.classList.remove('hidden');
        } else {
            target_div.classList.add('hidden');
        }
    } else {
        target_div.classList.add('hidden');
    }
}

function updateItemDiv(e) {
    target_div = document.getElementById(e.name);

    target_img = document.querySelector("#"+e.name+'_img img');
    race_img = document.getElementById(e.name+'_img_race');
    material_img = document.getElementById(e.name+'_img_material');
    target_name = document.getElementById(e.name+'_name');
    target_desc = document.getElementById(e.name+'_desc');

    buy = document.getElementById(e.name+'_buy');
    sell = document.getElementById(e.name+'_sell');
    hp = document.getElementById(e.name+'_hp');
    phys_atk = document.getElementById(e.name+'_phys_atk');
    mag_atk = document.getElementById(e.name+'_mag_atk');
    phys_def = document.getElementById(e.name+'_phys_def');
    mag_def = document.getElementById(e.name+'_mag_def');
    acc = document.getElementById(e.name+'_acc');
    res = document.getElementById(e.name+'_res');
    ign_phys = document.getElementById(e.name+'_ign_phys');
    ign_mag = document.getElementById(e.name+'_ign_mag');
    speed = document.getElementById(e.name+'_speed');
    crit_rate = document.getElementById(e.name+'_crit_rate');
    crit_dmg = document.getElementById(e.name+'_crit_dmg');


    item = items.filter(item => item.pk.toString() === e.value)[0];
    if (item) {
        item_fields = item.fields;

        if (item_fields) {
            item_color = "text-" + tiers_colors[item_fields.tier];

            target_img.src = media_url+item_fields.img;
            race_img.src = media_url+item_fields.race[0];
            material_img.src = media_url+item_fields.material[0];

            target_name.innerHTML = item_fields.name;
            target_name.classList.add(item_color);

            target_desc.innerHTML = item_fields.desc;

            buy.innerHTML = item_fields.buy_cost
            sell.innerHTML = item_fields.sell_cost

            hp.innerHTML = item_fields.hp
            phys_atk.innerHTML = item_fields.phys_atk
            mag_atk.innerHTML = item_fields.mag_atk
            phys_def.innerHTML = item_fields.phys_def
            mag_def.innerHTML = item_fields.mag_def
            acc.innerHTML = item_fields.acc
            res.innerHTML = item_fields.res
            ign_phys.innerHTML = item_fields.ign_phys
            ign_mag.innerHTML = item_fields.ign_mag
            speed.innerHTML = item_fields.speed
            crit_rate.innerHTML = item_fields.crit_rate
            crit_dmg.innerHTML = item_fields.crit_dmg

            target_div.classList.remove('hidden');
        } else {
            target_div.classList.add('hidden');
        }
    } else {
        target_div.classList.add('hidden');
    }
}